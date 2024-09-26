import pystac

from utils.logging_config import logger
from utils import raster, storage, stac_rest
from datetime import datetime, timedelta
from sys import exit as sysexit
from urllib import parse
from os import remove, rmdir, path, makedirs
from config import get_settings


class Collection:

    def __init__(self):
        self.items = []
        self.dates = []
        self.longs = []
        self.lats = []
        self.stac_collection = []
        self.stac_items = []
        self.stac_url = get_settings().stac_url
        self.storage = storage.Storage()

    def load_items(self, folder, raw_items):
        """
        Prepare items data and get attributes for collection creation.
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

            # Preparing item data
            item_data["year"] = item["year"]
            item_data["id"] = item["id"]
            item_data["input_file"] = item["assets"]["input_file"]
            item_data["datetime"] = datetime(
                int(item["year"]) + 1, 1, 1
            ) - timedelta(days=1)
            item_data["properties"] = (
                item["properties"] if "properties" in item else {}
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
        )

        self.stac_collection.validate()
        logger.info(f"Collection {collection_id} validated successfully")

        return collection_id

    def create_items(self):
        """
        Validate item creation.
        """
        if self.items:
            for item_data in self.items:
                item = pystac.Item(
                    id=item_data["id"],
                    geometry=item_data["footprint"],
                    bbox=item_data["bbox"],
                    datetime=item_data["datetime"],
                    properties=item_data["properties"],
                )
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
                    "To overwrite it, rerun the program \n"
                    "with the -o parameter.\n"
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
            raise RuntimeError(f"Missing collection id to remove")

        collection_url = f"{self.stac_url}/collections/{collection_id}"
        logger.info(f"Attempting to remove collection {collection_id}")

        try:
            items_collection = stac_rest.get(f"{collection_url}/items").json()
            for item in items_collection["features"]:
                for asset_key, asset_value in item["assets"].items():
                    parsed_url = parse.urlparse(asset_value["href"])
                    blob_url = parsed_url.path.split("/")[-1]
                    logger.info(
                        f"Deleting file: {blob_url} from Azure Blob Storage"
                    )
                    self.storage.remove_file(blob_url)

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
            stac_rest.post_or_put(
                parse.urljoin(self.stac_url, "/collections"),
                self.stac_collection.to_dict(),
            )

            for item in self.stac_items:
                stac_rest.post_or_put(
                    parse.urljoin(
                        self.stac_url,
                        f"/collections/{self.stac_collection.id}/items",
                    ),
                    item.to_dict(),
                )
        except Exception as e:
            raise RuntimeError(f"Error uploading collection: {e}")

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
        if self.items:
            for i, item in enumerate(self.items):
                file_path = path.join(output_folder, item["input_file"])

                collection_name = self.stac_collection.id

                final_url = self.storage.upload_file(
                    f"{collection_name}/{item['input_file']}", file_path
                )

                if final_url:
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
