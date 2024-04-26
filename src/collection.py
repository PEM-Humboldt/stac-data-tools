import pystac
from utils import raster
from datetime import datetime, timedelta


class Collection:

    def __init__(self):
        self.items = []
        self.dates = []
        self.longs = []
        self.lats = []

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
        collection_id = (
            collection_name
            if collection_name is not None
            else collection_data["id"]
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

        collection = pystac.Collection(
            id=collection_id,
            title=collection_data["title"],
            description=collection_data["description"],
            extent=pystac.Extent(
                spatial=spatial_extent,
                temporal=temporal_extent,
            ),
        )

        collection.validate()

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

                item.validate()
