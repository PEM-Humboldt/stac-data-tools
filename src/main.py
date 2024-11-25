from argparse import ArgumentParser

from utils.logging_config import logger
from pypgstac.db import settings
from utils import spec
from utils.auth import authenticate
from collection import Collection
from json import load
from sys import exit as sysexit
from os import getcwd
from config import get_settings

settings = get_settings()


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
    parser.add_argument(
        "-u", "--username", required=True, help="Username for authentication"
    )
    parser.add_argument(
        "-p", "--password", required=True, help="Password for authentication"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    create_parser = subparsers.add_parser("create", help="Create a collection")
    create_parser.add_argument(
        "-f", "--folder", required=True, help="Input folder"
    )
    create_parser.add_argument("-c", "--collection", help="Collection name")
    create_parser.add_argument(
        "-o", "--overwrite", action="store_true", help="Overwrite"
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a collection"
    )
    validate_parser.add_argument(
        "-f", "--folder", required=True, help="Input folder"
    )
    validate_parser.add_argument("-c", "--collection", help="Collection name")

    remove_parser = subparsers.add_parser("remove", help="Remove a collection")
    remove_parser.add_argument(
        "-c", "--collection", required=True, help="Collection name"
    )

    try:
        args = parser.parse_args()

        token = authenticate(
            args.username, args.password, settings.stac_url, settings.auth_url
        )

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

        elif args.command == "validate":
            input_folder = f"input/{args.folder}"
            create_collection_local(collection, input_folder, args.collection)
            logger.info("Validation successful.")

        elif args.command == "remove":
            collection.remove_collection(args.collection)
            logger.info("Collection removed successfully.")

        else:
            sysexit("No command used. Type -h for help")

    except SystemExit as e:
        logger.info("Error en los argumentos:", e)


if __name__ == "__main__":
    main()
