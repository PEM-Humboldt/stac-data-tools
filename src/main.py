from argparse import ArgumentParser
from utils.logging_config import logger
from utils import spec
from utils.auth import authenticate
from collection import Collection
from json import load
from sys import exit as sysexit
from os import getcwd


def create_collection_local(collection, input_folder, collection_name):
    spec.validate_input_folder(input_folder)

    with open(f"{input_folder}/collection.json", "r") as f:
        data = load(f)
        raw_items = [item for item in data["items"]]

    spec.validate_format(data)
    spec.validate_layers(input_folder, raw_items)

    collection.load_items(input_folder, raw_items)

    collection.create_collection(collection_name, data)
    logger.info("Collection created successfully.")

    collection.create_items()
    logger.info("Items created successfully.")


def main():
    parser = ArgumentParser(description="STAC Collection Manager")
    sub_parsers = parser.add_subparsers(dest="command", help="Commands")

    create_parser = sub_parsers.add_parser(
        "create", help="Create a new collection"
    )
    create_parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        help="Collection folder",
        required=True,
    )
    create_parser.add_argument(
        "-c",
        "--collection",
        dest="collection",
        help="Collection name",
        required=False,
    )
    create_parser.add_argument(
        "-o",
        "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Overwrite existing collection",
        required=False,
    )

    validate_parser = sub_parsers.add_parser(
        "validate", help="Validate collection specification"
    )
    validate_parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        help="Collection folder",
        required=True,
    )
    validate_parser.add_argument(
        "-c",
        "--collection",
        dest="collection",
        help="Collection name",
        required=False,
    )

    remove_parser = sub_parsers.add_parser(
        "remove", help="Remove indicated collection"
    )
    remove_parser.add_argument(
        "-c",
        "--collection",
        dest="collection",
        help="Collection name",
        required=True,
    )

    args = parser.parse_args()

    token = authenticate()

    collection = Collection(token)

    if args.command == "create":
        input_folder = f"input/{args.folder}"
        create_collection_local(collection, input_folder, args.collection)

        if collection.check_collection(args.overwrite):
            collection.remove_collection()
            logger.info("Previous collection removed.")

        output_dir = f"{getcwd()}/output/{args.folder}"
        collection.convert_layers(input_folder, output_dir)
        logger.info("Layers converted successfully.")

        collection.upload_layers(output_dir)
        collection.upload_collection()
        logger.info("Collection uploaded successfully.")

        sysexit("Process completed successfully.")

    elif args.command == "validate":
        create_collection_local(
            collection, f"input/{args.folder}", args.collection
        )
        logger.info("Validation successful.")

    elif args.command == "remove":
        collection.remove_collection(args.collection)
        logger.info("Collection removed successfully.")

    else:
        sysexit("No command used. Type -h for help")


if __name__ == "__main__":
    main()
