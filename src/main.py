from argparse import ArgumentParser

from utils.logging_config import logger
from utils import spec
from utils.auth import authenticate
from json import load
from sys import exit as sysexit
from os import getcwd
from collection import Collection, update_collection_json_inplace


def create_collection_local(collection, input_folder, collection_name):
    """Read and validate local collection.json, load items, and build pystac objects."""
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

    inject_parser = sub_parsers.add_parser(
        "inject",
        help="Inject items into input/<folder>/collection.json from .tif files in that folder (overwrite file)",
    )
    inject_parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        required=True,
        help="Folder name under 'input/' containing collection.json and .tif files (e.g., LossPersistence)",
    )
    inject_parser.add_argument(
        "-o",
        "--output",
        dest="output",
        required=False,
        help="Optional output path to write the resulting JSON elsewhere (otherwise overwrite in place)",
    )
    inject_parser.add_argument(
        "--no-backup",
        dest="no_backup",
        action="store_true",
        help="Do not create a backup when overwriting collection.json",
    )

    args = parser.parse_args()

    authenticate()
    collection = Collection()

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
        logger.info("Layers uploaded successfully.")

        collection.upload_collection()
        logger.info("Collection uploaded successfully.")

        sysexit("Process completed successfully.")

    elif args.command == "validate":
        create_collection_local(
            collection, f"input/{args.folder}", args.collection
        )
        sysexit("Validation successful.")

    elif args.command == "remove":
        collection.remove_collection(args.collection)
        sysexit("Collection removed successfully.")

    elif args.command == "inject":

        input_folder = f"input/{args.folder}"

        output_path = args.output

        make_backup = not args.no_backup

        backup_dir = f"{getcwd()}/output/{args.folder}/_backups"

        update_collection_json_inplace(
            input_folder=input_folder,
            output_path=output_path,
            make_backup=make_backup,
            backup_dir=backup_dir,
        )

        sysexit("Items injected and collection.json overwritten successfully.")

    else:
        sysexit("No command used. Type -h for help")


if __name__ == "__main__":
    main()
