from argparse import ArgumentParser
from utils import spec
from collection import Collection
from json import load
from sys import exit as sysexit
from dotenv import load_dotenv
from os import getenv


def main():
    """
    Read arguments and start data validation.
    """

    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        help="Collection folder",
        required=True,
    )

    parser.add_argument(
        "-c",
        "--collection",
        dest="collection",
        help="Collection name",
        required=False,
    )

    parser.add_argument(
        "-v",
        "--validate-only",
        dest="validation",
        action="store_true",
        help="Only validation",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Overwrite existing collection",
        required=False,
    )

    args = parser.parse_args()
    folder = "input/" + args.folder
    collection_name = args.collection
    validation = args.validation
    overwrite = args.overwrite

    load_dotenv()
    if getenv("STAC_URL"):
        stac_url = getenv("STAC_URL")

    abs_config = {}
    if getenv("ABS_STRING"):
        abs_config["string"] = getenv("ABS_STRING")

    if getenv("ABS_STRING"):
        abs_config["container"] = getenv("ABS_CONTAINER")

    spec.validate_input_folder(folder)

    with open("{}/collection.json".format(folder), "r") as f:
        data = load(f)
        raw_items = [item for item in data["items"]]

    spec.validate_format(data)
    spec.validate_layers(folder, raw_items)

    collection = Collection(stac_url, collection_name, data)
    collection.load_items(folder, raw_items)
    collection.create_collection(collection_name, data)
    collection.create_items()

    if validation:
        sysexit("Successful validation.")

    if collection.check_collection(overwrite):
        collection.remove_collection()

    output_dir = f"output/{collection_name}"
    collection.convert_layers(folder, output_dir)
    collection.upload_layers(abs_config, output_dir)
    collection.upload_collection()


if __name__ == "__main__":
    main()
