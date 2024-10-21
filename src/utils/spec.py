from os import path, listdir
from json import load
from jsonschema import validate, FormatError


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
    print("Cargando el esquema JSON de la colección...")
    with open("spec/collection.json", "r") as f:
        schema = load(f)
    try:
        validate(instance=data, schema=schema)

        if "metadata" in data and "properties" in data["metadata"]:
            metadata_properties_lengths = [
                len(data["metadata"]["properties"][key])
                for key in data["metadata"]["properties"]
            ]
            if len(set(metadata_properties_lengths)) != 1:
                raise FormatError(
                    "Error en las propiedades de la colección: "
                    "Los elementos dentro de 'metadata.properties' no tienen la misma longitud."
                )

        for item in data.get("items", []):
            if "properties" not in item:
                raise FormatError(
                    f"El item '{item['id']}' no contiene el campo 'properties'."
                )

            item_properties_lengths = []
            for key in item["properties"]:
                if not isinstance(item["properties"][key], list):
                    raise FormatError(
                        f"El item '{item['id']}' tiene 'properties.{key}' que no es una lista."
                    )
                length = len(item["properties"][key])
                item_properties_lengths.append(length)

            if len(set(item_properties_lengths)) != 1:
                raise FormatError(
                    f"Error en las propiedades del item '{item['id']}': "
                    "Las propiedades no tienen la misma longitud."
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
