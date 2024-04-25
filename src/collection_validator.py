import pystac
from utils import get_tif_metadata
from datetime import datetime, timedelta


class CollectionValidator:

    def __init__(self, folder, collection_data, collection_name, items):
        self.collection_data = collection_data
        self.collection_name = collection_name
        self.raw_items = items
        self.folder = folder

    def load_items(self):
        """
        Prepare items data and get attributes for collection creation.
        """

        self.items = []
        self.dates = []
        self.longs = []
        self.lats = []
        for item in self.raw_items:
            item_data = {}
            file_path = "{}/{}".format(
                self.folder, item["assets"]["input_file"]
            )
            (
                item_data["bbox"],
                item_data["footprint"],
                item_data["crs"],
                item_data["resolution"],
                item_data["dtype"],
            ) = get_tif_metadata(file_path)

            item_data["year"] = item["year"]
            item_data["id"] = item["id"]
            item_data["input_file"] = item["assets"]["input_file"]
            item_data["datetime"] = datetime(
                int(item["year"]) + 1,
                1,
                1,
            ) - timedelta(days=1)

            self.items.append(item_data)
            self.dates.append(item["year"])
            self.longs.append(item_data["bbox"][0])
            self.longs.append(item_data["bbox"][2])
            self.lats.append(item_data["bbox"][1])
            self.lats.append(item_data["bbox"][3])

    def create_collection(self):
        """
        Set the parameters and create an initial collection
        """
        self.collection_id = (
            self.collection_name
            if self.collection_name is not None
            else self.data["id"]
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

        self.collection = pystac.Collection(
            id=self.collection_id,
            title=self.collection_data["title"],
            description=self.collection_data["description"],
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
        for item_data in self.items:
            item = pystac.Item(
                id=item_data["id"],
                geometry=item_data["footprint"],
                bbox=item_data["bbox"],
                datetime=item_data["datetime"],
                properties={},
            )

            item.validate()
