import os
import sys
import json
from jsonschema import validate
import argparse
import pystac
import utils
from datetime import datetime, timedelta
from urllib import parse


class CheckCollection:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-f",
            "--folder",
            dest="folder",
            help="Collection folder",
            required=True,
        )

        parser.add_argument(
            "-s",
            "--server",
            dest="server",
            help="Server URL",
            required=True,
        )

        parser.add_argument(
            "-c",
            "--collection",
            dest="collection",
            help="Collection name",
            required=False,
        )

        args = parser.parse_args()
        self.folder = "input/" + args.folder
        self.collection_name = args.collection
        self.server = args.server

        self.read_collection()
        self.load_data()
        self.format_check()
        self.layers_check()
        self.load_items()
        self.create_collection()
        self.create_items()

    def read_collection(self):
        """
        Check if the collection folder exists and contains the collection file
        """
        if not (
            os.path.exists(self.folder)
            and "collection.json" in os.listdir(self.folder)
        ):
            print(
                "El directorio no existe o no contiene el archivo collection.json."
            )
            sys.exit()

    def load_data(self):
        # Load the JSON file
        with open("{}/collection.json".format(self.folder), "r") as f:
            self.data = json.load(f)
            self.items = [item for item in self.data["items"]]

    def format_check(self):
        """
        Check if the collection.json file has the defined format
        """
        with open("input/stac_spec.json", "r") as f:
            schema = json.load(f)

        try:
            validate(instance=self.data, schema=schema)
            print("JSON is valid against the schema.")
        except Exception as e:
            print("JSON is not valid against the schema:", e)
            sys.exit()

    def layers_check(self):
        """
        Check if the layer files exist
        """
        for item in self.items:
            file_path = "{}/{}".format(
                self.folder, item["assets"]["input_file"]
            )
            if os.path.exists(file_path):
                print(f"The file '{file_path}' exists.")
            else:
                print(f"The file '{file_path}' does not exist.")

    def load_items(self):
        """
        Read a json file with information about a collection an features
        Convert TIF files to COG and upload them to Azure Blob Storage
        Extract information to create STAC collection an items
        """

        self.items_collection = []
        self.dates = []
        self.longs = []
        self.lats = []
        for item in self.items:
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
            ) = utils.get_tif_metadata(file_path)

            item_data["year"] = item["year"]
            item_data["id"] = item["id"]
            item_data["input_file"] = item["assets"]["input_file"]
            item_data["datetime"] = datetime(
                int(item["year"]) + 1,
                1,
                1,
            ) - timedelta(days=1)

            self.items_collection.append(item_data)
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
            title=self.data["title"],
            description=self.data["description"],
            extent=pystac.Extent(
                spatial=spatial_extent,
                temporal=temporal_extent,
            ),
        )

        try:
            utils.post_or_put(
                parse.urljoin(self.server, "/collections"),
                self.collection.to_dict(),
            )
            print("Collection created.")
        except Exception as e:
            print("Error creating the collection:", e)
            sys.exit()

    def create_items(self):
        """
        Create items an upload to collection
        """
        for item_data in self.items_collection:

            item = pystac.Item(
                id=item_data["id"],
                geometry=item_data["footprint"],
                bbox=item_data["bbox"],
                datetime=item_data["datetime"],
                properties={},
                collection=self.collection_id,
            )

            try:
                utils.post_or_put(
                    f"{self.server}/collections/{self.collection_id}/items",
                    item.to_dict(),
                )
                print("Item created.")
            except Exception as e:
                print("Error creating the item:", e)
                sys.exit()


stac = CheckCollection()
