from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    RawTextHelpFormatter,
)



class SmartFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    pass


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="sdt",  # hará que el usage muestre "sdt" en lugar de __main__.py
        description="STAC Collection Manager",
        formatter_class=SmartFormatter,
    )

    sub_parsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="{create,validate,remove,inject}",
    )
    # obliga a elegir un subcomando (evita silent no-op)
    sub_parsers.required = True

    # -----------------------
    # create
    # -----------------------
    create_parser = sub_parsers.add_parser(
        "create",
        help="Create a new STAC collection",
        description=(
            "Create a new STAC collection from files in input/[folder}.\n\n"
            "What it does:\n"
            "  1) Validates folder structure and collection.json\n"
            "  2) Converts raster layers to Cloud Optimized \n"
            "GeoTIFF (COG)\n"
            "  3) Uploads layers and the collection to the \n"
            "configured storage\n"
            "  4) (Optional) Cleans local COGs after a successful \n"
            "upload\n\n"
            "Examples:\n"
            "  sdt create -f my_folder -c MyCollection\n"
            "  sdt create --folder my_folder --collection MyCollection\n"
            "  sdt create -f my_folder --delete-local-cog\n"
        ),
        formatter_class=SmartFormatter,
    )
    create_parser.add_argument(
        "-f",
        "--folder",
        required=True,
        dest="folder",
        metavar="FOLDER_NAME",
        help="Input folder under 'input/' containing \n"
             "collection.json and data layers.",
    )
    create_parser.add_argument(
        "-c",
        "--collection",
        required=False,
        dest="collection",
        metavar="COLLECTION_NAME",
        help="Collection name. If omitted, the 'id' \n"
             "from collection.json is used.",
    )
    create_parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        dest="overwrite",
        help="Overwrite the existing collection \n"
             "if it already exists.",
    )
    create_parser.add_argument(
        "--delete-local-cog",
        action="store_true",
        dest="delete_local_cog",
        help=(
            "Delete local COGs from output/{folder} \n"
            "after a successful upload.If the output folder becomes empty, \n"
            "it will be removed as well."
        ),
    )

    # -----------------------
    # validate
    # -----------------------
    validate_parser = sub_parsers.add_parser(
        "validate",
        help="Validate a collection specification",
        description=(
            "Validate the folder structure and the collection.json \n"
            "schema without converting or uploading data.\n\n"
            "Examples:\n"
            "  sdt validate -f my_folder\n"
            "  sdt validate --folder my_folder -c MyCollection\n"
        ),
        formatter_class=SmartFormatter,
    )
    validate_parser.add_argument(
        "-f",
        "--folder",
        required=True,
        dest="folder",
        metavar="FOLDER_NAME",
        help="Input folder under 'input/' containing \n"
             "collection.json and data layers.",
    )
    validate_parser.add_argument(
        "-c",
        "--collection",
        required=False,
        dest="collection",
        metavar="COLLECTION_NAME",
        help="Collection name to validate. If omitted, \n"
             "the 'id' from collection.json is used.",
    )

    # -----------------------
    # remove
    # -----------------------
    remove_parser = sub_parsers.add_parser(
        "remove",
        help="Remove a collection",
        description=(
            "Remove the indicated collection from the target \n"
            "storage.\n\n"
            "Examples:\n"
            "  sdt remove -c MyCollection\n"
            "  sdt remove --collection MyCollection\n"
        ),
        formatter_class=SmartFormatter,
    )
    remove_parser.add_argument(
        "-c",
        "--collection",
        required=True,
        dest="collection",
        metavar="COLLECTION_NAME",
        help="Collection name to remove.",
    )

    # -----------------------
    # inject
    # -----------------------
    inject_parser = sub_parsers.add_parser(
        "inject",
        help="Inject items into collection.json from .tif files",
        description=(
            "Scan input/{folder} for .tif files and rewrite \n"
            "the 'items' array in. "
            "input/{folder}/collection.json. The rest of the \n"
            "fields remain unchanged."
            "Important:\n"
            "  - .tif filenames must include a year (e.g., 2005) \n"
            "or a period (e.g., 2000_2005 or 2000-2005)\n"
            "  - Duplicate year/period entries will raise an error\n\n"
            "Examples:\n"
            "  sdt inject -f my_folder            # with backup\n"
            "  sdt inject -f my_folder --no-backup\n"
        ),
        formatter_class=SmartFormatter,
    )
    inject_parser.add_argument(
        "-f",
        "--folder",
        required=True,
        dest="folder",
        metavar="FOLDER_NAME",
        help="Folder under 'input/' containing \n"
             "collection.json and .tif files.",
    )
    inject_parser.add_argument(
        "-o",
        "--output",
        required=False,
        dest="output",
        metavar="PATH",
        help="Optional output path for the resulting JSON \n"
             "(default: overwrite input collection.json).",
    )
    inject_parser.add_argument(
        "--no-backup",
        action="store_true",
        dest="no_backup",
        help="Do not create a backup when overwriting \n"
             "collection.json.",
    )

    return parser
