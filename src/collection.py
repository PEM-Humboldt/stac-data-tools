import json
import os
import re
from copy import deepcopy
from datetime import datetime, timedelta
from os import makedirs, path, remove, rmdir
from sys import exit as sysexit
from urllib import parse

import pystac
import rasterio
from pystac.extensions.projection import ProjectionExtension

from config import get_settings
from utils import raster, stac_rest, storage
from utils.logging_config import logger


class Collection:

    def __init__(self):
        self.uploaded_urls = []
        self.items = []
        self.dates = []
        self.longs = []
        self.lats = []
        self.stac_collection: pystac.Collection
        self.stac_items = []
        self.stac_url = get_settings().stac_url
        self.storage = storage.Storage()

    def load_items(self, folder, raw_items):
        """
        Prepare items data and get attributes for collection creation.
        Respect an existing 'proj:epsg' in properties; compute it only if missing.
        Fail fast if EPSG cannot be resolved (required by downstream tools).
        """
        logger.info(f"Loading items from {folder}")

        for item in raw_items:
            item_data = {}
            file_path = f"{folder}/{item['assets']['input_file']}"
            logger.info(f"Retrieving metadata from file: {file_path}")

            (
                item_data["bbox"],
                item_data["footprint"],
                item_data["crs"],
                item_data["resolution"],
                item_data["dtype"],
            ) = raster.get_tif_metadata(file_path)

            item_data["year"] = item["year"]
            item_data["id"] = item["id"]
            item_data["input_file"] = item["assets"]["input_file"]
            item_data["datetime"] = datetime(
                int(item["year"]) + 1, 1, 1
            ) - timedelta(days=1)
            item_data["properties"] = (
                item["properties"] if "properties" in item else {}
            )

            existing_epsg = item_data["properties"].get("proj:epsg")
            epsg: int | None = None
            if isinstance(existing_epsg, int) and existing_epsg > 0:
                epsg = existing_epsg
                logger.info(
                    f"Keeping existing proj:epsg={epsg} for item {item_data['id']}"
                )
            else:

                try:
                    with rasterio.open(file_path) as src:
                        epsg = src.crs.to_epsg() if src.crs else None
                except Exception as e:
                    logger.info(
                        f"Could not get EPSG via rasterio for {file_path}: {e}"
                    )

                if epsg is None:
                    crs_code = item_data["crs"]
                    if isinstance(crs_code, dict) and "init" in crs_code:
                        try:
                            epsg = int(str(crs_code["init"]).split(":")[1])
                        except Exception:
                            epsg = None
                    elif isinstance(crs_code, int):
                        epsg = crs_code

                if epsg is not None:
                    logger.info(
                        f"Computed proj:epsg={epsg} for item {item_data['id']}"
                    )
                    item_data["properties"]["proj:epsg"] = int(epsg)

            if epsg is None:
                raise ValueError(
                    f"Missing proj:epsg for item {item_data['id']} (file: {file_path}, CRS: {item_data['crs']})"
                )

            self.items.append(item_data)
            self.dates.append(item["year"])
            self.longs.extend([item_data["bbox"][0], item_data["bbox"][2]])
            self.lats.extend([item_data["bbox"][1], item_data["bbox"][3]])

        logger.info("Items loaded successfully")

    def create_collection(self, collection_name, collection_data):
        """
        Set the parameters and create an initial collection.
        """
        logger.info(
            f"Creating collection {collection_name or collection_data['id']}"
        )

        bboxes = [
            min(self.longs),
            min(self.lats),
            max(self.longs),
            max(self.lats),
        ]
        spatial_extent = pystac.SpatialExtent(bboxes=[bboxes])
        temporal_extent = pystac.TemporalExtent(
            intervals=[
                [
                    datetime(int(min(self.dates)), 1, 1),
                    datetime(int(max(self.dates)) + 1, 1, 1)
                    - timedelta(days=1),
                ]
            ]
        )

        collection_id = (
            collection_name
            if collection_name is not None
            else collection_data["id"]
        )

        self.stac_collection = pystac.Collection(
            id=collection_id,
            title=collection_data["title"],
            description=collection_data["description"],
            extent=pystac.Extent(
                spatial=spatial_extent, temporal=temporal_extent
            ),
            extra_fields={"metadata": collection_data["metadata"]},
        )

        self.stac_collection.validate()
        logger.info(f"Collection {collection_id} validated successfully")

        return collection_id

    def create_items(self):
        if self.items:
            for item_data in self.items:
                if "proj:epsg" not in item_data["properties"]:
                    raise ValueError(
                        f"Item {item_data['id']} is missing proj:epsg"
                    )

                item = pystac.Item(
                    id=item_data["id"],
                    geometry=item_data["footprint"],
                    bbox=item_data["bbox"],
                    datetime=item_data["datetime"],
                    properties=item_data["properties"],
                )
                ProjectionExtension.add_to(item)
                ProjectionExtension.ext(item).epsg = item_data["properties"][
                    "proj:epsg"
                ]
                item.stac_extensions = [
                    "https://stac-extensions.github.io/projection/v1.0.0/schema.json"
                ]
                item.validate()
                self.stac_items.append(item)

    def check_collection(self, overwritten):
        """
        Check if the collection exists and if it's going to be overwritten.
        """
        url = f"{self.stac_url}/collections/{self.stac_collection.id}"
        exist = stac_rest.check_resource(url)
        if exist:
            collection_exist = True
            if not overwritten:
                sysexit(
                    f"Collection {self.stac_collection.id} already exists.\n"
                    "To overwrite it, rerun the program with the -o parameter.\n"
                    "For more help, use the -h parameter."
                )
        else:
            collection_exist = False
        return collection_exist

    def remove_collection(self, collection_name=None):
        """
        Remove collection from STAC server and Azure Blob Storage.
        """
        collection_id = collection_name
        if (
            hasattr(self, "stac_collection")
            and self.stac_collection.id is not None
        ):
            collection_id = self.stac_collection.id
        if collection_id is None:
            raise RuntimeError("Missing collection id to remove")

        collection_url = f"{self.stac_url}/collections/{collection_id}"
        logger.info(f"Attempting to remove collection {collection_id}")

        try:
            items_response = stac_rest.get(f"{collection_url}/items")
            items = items_response.json().get("features", [])

            for item in items:
                for asset_key, asset_value in item["assets"].items():
                    url = asset_value["href"]
                    logger.info(f"Deleting file {url} from Azure Blob Storage")
                    self.storage.remove_file(url)

            stac_rest.delete(collection_url)
            logger.info(f"Collection {collection_id} removed successfully")

        except Exception as e:
            logger.error(f"Error removing collection from server: {e}")
            raise RuntimeError(f"Error removing collection from server: {e}")

    def upload_collection(self):
        """
        Upload the collection and items to the STAC server.
        """
        try:
            logger.info(
                f"Uploading collection: {self.stac_collection.to_dict()}"
            )

            stac_rest.post_or_put(
                parse.urljoin(self.stac_url, "/collections"),
                self.stac_collection.to_dict(),
            )
            logger.info(
                f"Collection {self.stac_collection.id} uploaded successfully"
            )

            for item in self.stac_items:
                item_dict = item.to_dict()
                item_response = stac_rest.post_or_put(
                    parse.urljoin(
                        self.stac_url,
                        f"/collections/{self.stac_collection.id}/items",
                    ),
                    item_dict,
                )
                logger.info(
                    f"Item upload response: {item_response.status_code}"
                )

        except Exception as e:
            logger.error(f"Error uploading collection: {e}")

            for url in self.uploaded_urls:
                try:
                    self.storage.remove_file(url)
                    logger.info(f"Removed uploaded file: {url}")
                except Exception as cleanup_error:
                    logger.error(
                        f"Error cleaning up uploaded file {url}: {cleanup_error}"
                    )

            raise RuntimeError(f"Failed to upload collection: {e}")

    def convert_layers(self, input_dir, output_dir):
        """
        Convert item layers format and ensure the output directory exists.
        """
        if not path.exists(output_dir):
            makedirs(output_dir)
            logger.info(f"Directory created: {output_dir}")

        for i, item in enumerate(self.items):
            logger.info(f"Converting {item['input_file']} to COG")
            raster.tif_to_cog(item["input_file"], input_dir, output_dir)
            logger.info(f"Conversion of {item['input_file']} completed")

    def upload_layers(self, output_folder):
        """
        Upload item layers to storage.
        """
        self.uploaded_urls = []
        if self.items:
            for i, item in enumerate(self.items):
                logger.info(f"Uploading {item['input_file']}")
                file_path = path.join(output_folder, item["input_file"])

                collection_name = self.stac_collection.id

                final_url = self.storage.upload_file(
                    f"{collection_name}/{item['input_file']}", file_path
                )

                if final_url:
                    self.uploaded_urls.append(final_url)
                    remove(file_path)

                self.stac_items[i].add_asset(
                    key=item["id"],
                    asset=pystac.Asset(
                        href=final_url,
                        media_type=pystac.MediaType.COG,
                    ),
                )
                self.stac_items[i].set_self_href(final_url)

            try:
                rmdir(output_folder)
            except Exception as e:
                raise RuntimeError(f"Error removing directory: {e}")


def update_collection_json_inplace(
    input_folder: str,
    output_path: str | None = None,
    make_backup: bool = True,
    backup_dir: str | None = None,
):
    """
    Read input/<folder>/collection.json, scan .tif files in that folder,
    create items from years/ranges in filenames:
      - If a range like '2006-2010' or '2006_2010' is found, the item id is '2006-2010'
        and 'year' will be the highest year ('2010').
      - If only single years are found, id = that year and 'year' = that same year.
    Overwrite collection.json injecting the generated 'items', or write to output_path.
    If backup_dir is provided, write the backup there; otherwise next to target.
    """
    abs_input = path.abspath(input_folder)
    if not path.isdir(input_folder):
        raise ValueError(f"Input folder does not exist: {abs_input}")

    template_path = path.join(input_folder, "collection.json")
    abs_template = path.abspath(template_path)
    if not path.isfile(template_path):
        raise FileNotFoundError(
            f"collection.json not found at: {abs_template}"
        )

    logger.info(f"Reading base collection from: {abs_template}")

    with open(template_path, "r", encoding="utf-8") as f:
        base = json.load(f)

    tif_files = [
        f for f in os.listdir(input_folder) if f.lower().endswith(".tif")
    ]
    if not tif_files:
        raise ValueError(f"No .tif files found in {abs_input}")

    logger.info(f"Found {len(tif_files)} .tif files in {abs_input}")

    range_pattern = re.compile(r"(?P<start>\d{4})\s*[-_]\s*(?P<end>\d{4})")
    year_pattern = re.compile(r"(\d{4})")

    items = []
    seen_ids = set()

    for tif_file in sorted(tif_files):
        rng = range_pattern.search(tif_file)
        if rng:
            start = int(rng.group("start"))
            end = int(rng.group("end"))
            if start > end:
                start, end = end, start
            item_id = f"{start}-{end}"
            year = str(end)
            logger.info(
                f"Detected period in filename '{tif_file}': id={item_id}, year={year}"
            )
        else:
            matches = year_pattern.findall(tif_file)
            if not matches:
                raise ValueError(
                    f"ERROR: '{tif_file}' does not contain a 4-digit year or year range. "
                    "Rename the file or adjust the detection pattern."
                )
            years = sorted({int(y) for y in matches})
            max_year = max(years)
            item_id = str(max_year)
            year = str(max_year)
            logger.info(
                f"Detected single year in filename '{tif_file}': id={item_id}, year={year}"
            )

        if item_id in seen_ids:
            raise ValueError(
                f"ERROR: Duplicate item id '{item_id}' derived from .tif files."
            )
        seen_ids.add(item_id)

        items.append(
            {"id": item_id, "year": year, "assets": {"input_file": tif_file}}
        )

    items.sort(key=lambda it: int(it["year"]))

    out = deepcopy(base)
    out["items"] = items

    target_path = output_path or template_path

    if make_backup and path.isfile(template_path):
        from datetime import datetime as _dt

        ts = _dt.now().strftime("%Y%m%d-%H%M%S")

        if backup_dir:
            dest_dir = backup_dir
        elif output_path:
            dest_dir = path.dirname(output_path) or "."
        else:
            dest_dir = input_folder

        os.makedirs(dest_dir, exist_ok=True)
        backup_path = path.join(dest_dir, f"collection.backup.{ts}.json")

        with open(backup_path, "w", encoding="utf-8") as fb:
            json.dump(base, fb, ensure_ascii=False, indent=2)
        logger.info(f"Backup saved at: {path.abspath(backup_path)}")

    os.makedirs(path.dirname(target_path) or ".", exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=2)

    logger.info(f"Collection JSON updated at: {path.abspath(target_path)}")
