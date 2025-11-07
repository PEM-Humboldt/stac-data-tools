from argparse import ArgumentParser
from json import load
from os import getcwd
from sys import exit as sysexit

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

    create_parser.add_argument(
        "--delete-local-cog",
        dest="delete_local_cog",
        action="store_true",
        help="(Opcional) Elimina los COG locales en la carpeta de salida luego de subirlos",
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

    add_item_parser = sub_parsers.add_parser(
        "add-item",
        help="Add a new item to an existing collection on the STAC server",
    )
    add_item_parser.add_argument(
        "-c",
        "--collection",
        dest="collection",
        required=True,
        help="Collection ID to add the item to",
    )
    add_item_parser.add_argument(
        "-f",
        "--folder",
        dest="folder",
        required=True,
        help="Folder name under 'input/' containing the .tif file",
    )
    add_item_parser.add_argument(
        "--file",
        dest="file",
        required=True,
        help="TIF filename to add as an item",
    )
    add_item_parser.add_argument(
        "--item-id",
        dest="item_id",
        help="Item ID (optional, will be inferred from filename if not provided)",
    )
    add_item_parser.add_argument(
        "--year",
        dest="year",
        required=True,
        help="Year associated with the item",
    )
    add_item_parser.add_argument(
        "--delete-local-cog",
        dest="delete_local_cog",
        action="store_true",
        help="(Optional) Delete local COG after upload",
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

        if args.delete_local_cog:
            collection.clean_local_cogs(output_dir)

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

    elif args.command == "add-item":
        from datetime import datetime

        from utils import raster

        # Get collection and existing items from server
        collection_data, existing_items = (
            collection.get_collection_from_server(args.collection)
        )

        # Process the new item file
        input_folder = f"input/{args.folder}"
        file_path = f"{input_folder}/{args.file}"

        logger.info(f"Processing file: {file_path}")

        # Get metadata from TIF file
        bbox, footprint, crs, resolution, dtype = raster.get_tif_metadata(
            file_path
        )

        # Get or infer EPSG
        epsg = None
        if isinstance(crs, int):
            epsg = crs
        else:
            logger.warning(f"Could not determine EPSG from CRS: {crs}")

        # Infer item ID from filename or use provided
        item_id = args.item_id or args.file.replace(".tif", "")

        # Create item data
        item_data = {
            "id": item_id,
            "year": args.year,
            "bbox": bbox,
            "footprint": footprint,
            "resolution": resolution,
            "dtype": dtype,
            "input_file": args.file,
            "datetime": datetime(int(args.year), 1, 1),
            "properties": {"proj:epsg": epsg} if epsg else {},
        }

        # Validate item against collection
        collection.validate_item_against_collection(
            item_data, collection_data, existing_items
        )

        # Use existing collection from server (convert dict to PySTAC Collection)
        from pystac import Collection as PySTACCollection

        collection.stac_collection = PySTACCollection.from_dict(
            collection_data
        )

        # Load and create the item
        collection.items = [item_data]
        collection.dates = [args.year]
        collection.longs = [bbox[0], bbox[2]]
        collection.lats = [bbox[1], bbox[3]]

        collection.create_items()

        # Convert to COG
        output_dir = f"{getcwd()}/output/{args.folder}"
        collection.convert_layers(input_folder, output_dir)
        logger.info("Layer converted to COG successfully.")

        # Upload layer and item
        collection.upload_layers(output_dir)
        logger.info("Layer uploaded successfully.")

        # Upload single item to server
        success = collection.upload_single_item(item_data)
        if success:
            logger.info(
                f"Item {item_id} added to collection {args.collection} successfully."
            )
        else:
            logger.error(
                f"Failed to add item {item_id} to collection {args.collection}"
            )
            sysexit(
                f"Error: Failed to add item {item_id} to collection {args.collection}"
            )

        if args.delete_local_cog:
            collection.clean_local_cogs(output_dir)

        sysexit(
            f"Item {item_id} added successfully to collection {args.collection}."
        )

    else:
        sysexit("No command used. Type -h for help")


if __name__ == "__main__":
    main()
