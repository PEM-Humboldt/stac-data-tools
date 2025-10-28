from enum import Enum
from json import load
from os import listdir, path

from jsonschema import FormatError, validate


class CollectionDataType(Enum):
    CONTINUOUS = "Continua"
    CLASSIFIED = "Clasificada"


def validate_input_folder(folder):
    """
    Check if the collection folder exists and contains the collection file.
    """
    if not (path.exists(folder) and "collection.json" in listdir(folder)):
        raise FileNotFoundError(
            f"El directorio {folder} no existe o "
            "no contiene el archivo collection.json."
        )


def validate_format(data):
    """
    Check if the collection.json file has the defined format
    """
    with open("spec/collection.json", "r") as f:
        schema = load(f)
    try:
        validate(instance=data, schema=schema)

        if "metadata" in data:
            data_type_values = [
                data_type.value for data_type in CollectionDataType
            ]

            data_type = data["metadata"]["data_type"]
            if data_type not in data_type_values:
                raise FormatError(
                    "Error en el tipo de dato de la colección 'metadata.data_type': "
                    f"El elemento debe tener uno de estos valores: {data_type_values}"
                )

            data_type_enum = CollectionDataType(data_type)

            if "properties" in data["metadata"]:
                if data_type_enum == CollectionDataType.CLASSIFIED:
                    properties = {
                        "values": data["metadata"]["properties"]["values"],
                        "colors": data["metadata"]["properties"]["colors"],
                        "classes": data["metadata"]["properties"]["classes"],
                    }

                    metadata_properties_lengths = [
                        len(data["metadata"]["properties"][property_name])
                        for property_name in properties
                    ]

                    if len(set(metadata_properties_lengths)) != 1:
                        raise FormatError(
                            "Error en las propiedades de la colección: "
                            "Los elementos dentro de 'metadata.properties' no tienen la misma longitud."
                        )

                if data_type_enum == CollectionDataType.CONTINUOUS:

                    if "class" not in data["metadata"]["properties"]:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.class': "
                            "El elemento no existe."
                        )

                    if len(data["metadata"]["properties"]["colors"]) != 3:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.colors': "
                            "La lista debe tener 3 elementos."
                        )

                    if len(data["metadata"]["properties"]["values"]) != 2:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.values': "
                            "La lista debe tener 2 elementos."
                        )

    except Exception as e:
        raise FormatError(
            f"El archivo no cumple con el formato JSON. Detalles: {e}"
        )


def validate_layers(folder, raw_items):
    """
    Check if the layer files exist
    """
    for item in raw_items:
        file_path = "{}/{}".format(folder, item["assets"]["input_file"])
        if not path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
