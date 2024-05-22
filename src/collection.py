import pystac
from utils import raster, storage, stac_rest
from datetime import datetime, timedelta
from sys import exit as sysexit
from urllib import parse


class Collection:

    def __init__(self, stac_url, collection_name, collection_data):
        self.items = []
        self.dates = []
        self.longs = []
        self.lats = []
        self.collection = []
        self.collection_id = []
        self.items_collection = []
        self.stac_url = stac_url

        self.collection_id = (
            collection_name
            if collection_name is not None
            else collection_data["id"]
        )

    def load_items(self, folder, raw_items):
        """
        Prepare items data and get attributes for collection creation.
        """

        for item in raw_items:
            item_data = {}
            file_path = "{}/{}".format(folder, item["assets"]["input_file"])
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
                int(item["year"]) + 1,
                1,
                1,
            ) - timedelta(days=1)
            item_data["properties"] = (
                item["properties"] if "properties" in item else {}
            )

            self.items.append(item_data)
            self.dates.append(item["year"])
            self.longs.append(item_data["bbox"][0])
            self.longs.append(item_data["bbox"][2])
            self.lats.append(item_data["bbox"][1])
            self.lats.append(item_data["bbox"][3])

    def create_collection(self, collection_name, collection_data):
        """
        Set the parameters and create an initial collection
        """

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

        self.collection = pystac.Collection(
            id=self.collection_id,
            title=collection_data["title"],
            description=collection_data["description"],
            extent=pystac.Extent(
                spatial=spatial_extent,
                temporal=temporal_extent,
            ),
        )

        self.collection.validate()

    def create_items(self):
        """
        Validate items creation
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
                if item.validate():
                    self.items_collection.append(item)

    def convert_layers(self, input_dir, output_dir):
        """
        Convert items layers format
        """
        for i, item in enumerate(self.items):
            self.items[i]["final_file"] = raster.tif_to_cog(
                item["input_file"], input_dir, output_dir
            )

    def check_collection(self, overwrite):
        """
        Check if the collection exists and if going to be overwriter
        """

        url = f"{self.stac_url}/collections/{self.collection_id}"
        exist = stac_rest.get(url)
        if exist:
            collection_exist = True
            if overwrite is False:
                sysexit(
                    f"La colección {self.collection_id} ya existe.\n"
                    "Si desea reemplazarla ejecute el programa nuevamente"
                    "con el parámetro -o.\n"
                    "Para más ayuda ejecute el script con el parámetro -h."
                )
        else:
            collection_exist = False
        return collection_exist

    def remove_collection(self):
        """
        Call to remove collection from STAC server
        """
        url = f"{self.stac_url}/collections/{self.collection_id}"
        stac_rest.delete(url)

    def upload_layers(self, abs_config, output_folder):
        """
        Upload items layers to storage
        """
        if self.items:
            for i, item in enumerate(self.items):
                final_url = storage.upload_file(
                    abs_config, output_folder, item["input_file"]
                )

                self.items_collection[i].add_asset(
                    key=item["id"],
                    asset=pystac.Asset(
                        href=final_url,
                        media_type=pystac.MediaType.COG,
                    ),
                )
                self.items_collection[i].set_self_href(final_url)

    def upload_collection(self):
        """
        Upload the colection and items to the STAC server
        """
        try:
            stac_rest.post_or_put(
                parse.urljoin(self.stac_url, "/collections"),
                self.collection.to_dict(),
            )

            for item in self.items_collection:
                stac_rest.post_or_put(
                    parse.urljoin(
                        self.stac_url,
                        f"/collections/{self.collection_id}/items",
                    ),
                    item.to_dict(),
                )
        except Exception as e:
            raise RuntimeError("Error al cargar la colección: {}".format(e))
