from json import load
from os import getcwd
from sys import exit as sysexit

from cli import build_parser
from collection import Collection, update_collection_json_inplace
from utils import spec
from utils.auth import authenticate
from utils.logging_config import logger


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
    parser = build_parser()
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
