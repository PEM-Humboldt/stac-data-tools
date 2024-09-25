from argparse import ArgumentParser

from utils.logging_config import logger
from utils import spec
from collection import Collection
from json import load
from sys import exit as sysexit
from os import getcwd


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
        required=False,
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

    parser.add_argument(
        "-r",
        "--remove-collection-by-name",
        dest="remove_collection_by_name",
        help="Name of the collection to remove",
        required=False,
    )

    args = parser.parse_args()

    if args.remove_collection_by_name:
        collection_id = args.remove_collection_by_name
        collection = Collection()
        collection.remove_collection_by_name(collection_id)
        sysexit("Collection successfully removed.")
    else:
        if not args.folder:
            sysexit(
                "The --folder argument is required if \n"
                "a collection is not being removed."
            )

        folder = "input/" + args.folder
        collection_name = args.collection
        validation = args.validation
        overwrite = args.overwrite

        spec.validate_input_folder(folder)

        with open(f"{folder}/collection.json", "r") as f:
            data = load(f)
            raw_items = [item for item in data["items"]]

        spec.validate_format(data)
        spec.validate_layers(folder, raw_items)

        collection = Collection()

        collection.load_items(folder, raw_items)

        collection.create_collection(collection_name, data)
        logger.info("Collection created successfully.")

        collection.create_items()
        logger.info("Items created successfully.")

        if validation:
            sysexit("Validation successful.")

        if collection.check_collection(overwrite):
            collection.remove_collection()
            sysexit("Previous collection removed successfully.")

        output_dir = f"{getcwd()}/output/{args.folder}"
        collection.convert_layers(folder, output_dir)
        logger.info("Layers converted successfully.")

        collection.upload_layers(output_dir)
        logger.info("Layers uploaded successfully.")

        collection.upload_collection()
        logger.info("Collection uploaded successfully.")

        sysexit("Process completed successfully.")


if __name__ == "__main__":
    main()
