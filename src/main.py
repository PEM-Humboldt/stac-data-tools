from argparse import ArgumentParser
from spec_validator import SpecValidator
from collection_validator import CollectionValidator


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
        "--validation",
        dest="validation",
        help="Only validation",
        required=False,
    )

    args = parser.parse_args()
    folder = "input/" + args.folder
    collection_name = args.collection

    spec_validator = SpecValidator(folder, collection_name)
    collection_data, items = spec_validator.load_data()
    spec_validator.validate_format()
    spec_validator.validate_layers()

    coleccion_validator = CollectionValidator(
        folder, collection_data, collection_name, items
    )
    coleccion_validator.load_items()
    coleccion_validator.create_collection()
    coleccion_validator.create_items()


if __name__ == "__main__":
    main()
