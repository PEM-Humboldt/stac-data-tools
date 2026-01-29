from enum import Enum
from json import load
from os import listdir, path
import re
import unicodedata

from jsonschema import FormatError, validate
from utils.constants import DOCS_URL
from utils.logging_config import logger


class CollectionDataType(Enum):
    CONTINUOUS = "Continua"
    CLASSIFIED = "Clasificada"


def _normalize_to_pascal_case(text):
    """
    Normalize text to PascalCase format.
    - Removes accents (á -> a, é -> e, etc.)
    - Removes spaces, underscores, hyphens
    - Capitalizes first letter of each word
    - Examples:
      - "huella_humana" -> "HuellaHumana"
      - "huella-humana" -> "HuellaHumana"
      - "huella humana" -> "HuellaHumana"
      - "huellaHumana" -> "HuellaHumana"
      - "HuellaHumana" -> "HuellaHumana" (already PascalCase)
    """
    if not isinstance(text, str):
        return text

    # Normalize to NFD (decomposed form) and remove combining diacritical marks
    normalized = unicodedata.normalize("NFD", text.strip())
    normalized = "".join(
        char
        for char in normalized
        if unicodedata.category(char) != "Mn"  # Mn = Nonspacing Mark
    )

    import re

    normalized = normalized.replace("_", " ").replace("-", " ")

    words = re.split(r"[\s_\-]+", normalized)
    words = [w for w in words if w]

    if not words:
        return text

    if len(words) == 1:
        single_word = words[0]
        if single_word[0].isupper() and re.search(r"[a-z][A-Z]", single_word):
            words = re.findall(r"[A-Z][a-z0-9]*", single_word)
        elif not single_word[0].isupper():
            words = [single_word]

    pascal_case = "".join(
        word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper()
        for word in words
    )

    return pascal_case


def validate_input_folder(folder):
    """
    Check if the collection folder exists and contains the collection file.
    """
    if not (path.exists(folder) and "collection.json" in listdir(folder)):
        raise FileNotFoundError(
            f"El directorio {folder} no existe o "
            "no contiene el archivo collection.json. "
            f"Para más información, consulte la documentación: {DOCS_URL}"
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
            if "projection" in data["metadata"]:
                projection = data["metadata"]["projection"]
                if "epsg" not in projection:
                    raise FormatError(
                        "Error en la proyección de la colección 'metadata.projection.epsg': "
                        "El elemento es requerido. "
                        f"Para más información, consulte la documentación: {DOCS_URL}"
                    )
                if (
                    not isinstance(projection["epsg"], int)
                    or projection["epsg"] < 1
                ):
                    raise FormatError(
                        "Error en la proyección de la colección 'metadata.projection.epsg': "
                        "Debe ser un número entero positivo. "
                        f"Para más información, consulte la documentación: {DOCS_URL}"
                    )

            data_type_values = [
                data_type.value for data_type in CollectionDataType
            ]

            data_type = data["metadata"]["data_type"]
            if data_type not in data_type_values:
                raise FormatError(
                    "Error en el tipo de dato de la colección 'metadata.data_type': "
                    f"El elemento debe tener uno de estos valores: {data_type_values}. "
                    f"Para más información, consulte la documentación: {DOCS_URL}"
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
                            "Los elementos dentro de 'metadata.properties' no tienen la misma longitud. "
                            f"Para más información, consulte la documentación: {DOCS_URL}"
                        )

                if data_type_enum == CollectionDataType.CONTINUOUS:

                    if "class" not in data["metadata"]["properties"]:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.class': "
                            "El elemento no existe. "
                            f"Para más información, consulte la documentación: {DOCS_URL}"
                        )

                    if len(data["metadata"]["properties"]["colors"]) != 3:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.colors': "
                            "La lista debe tener 3 elementos. "
                            f"Para más información, consulte la documentación: {DOCS_URL}"
                        )

                    if len(data["metadata"]["properties"]["values"]) != 2:
                        raise FormatError(
                            "Error en el metadato de la colección 'metadata.properties.values': "
                            "La lista debe tener 2 elementos. "
                            f"Para más información, consulte la documentación: {DOCS_URL}"
                        )

    except Exception as e:
        raise FormatError(
            f"El archivo no cumple con el formato JSON. Detalles: {e}. "
            f"Para más información, consulte la documentación: {DOCS_URL}"
        )


def validate_layers(folder, raw_items):
    """
    Check if the layer files exist
    """
    for item in raw_items:
        file_path = "{}/{}".format(folder, item["assets"]["input_file"])
        if not path.exists(file_path):
            raise FileNotFoundError(
                f"The file '{file_path}' does not exist. "
                f"Para más información, consulte la documentación: {DOCS_URL}"
            )


def validate_pre_upload(collection_data, collection_json_path):
    """
    Validate collection.json before uploading to ensure:
    - Proper JSON formatting
    - UTF-8 character encoding (no encoding issues with special characters)
    - Compliance with the standard defined in spec/collection.json

    Args:
        collection_data: Dictionary with collection data
        collection_json_path: Path to the collection.json file

    Raises:
        FormatError: If validation fails
    """
    try:
        import json

        json_str = json.dumps(collection_data, ensure_ascii=False, indent=2)
        json.loads(json_str)
    except (TypeError, ValueError) as e:
        raise FormatError(
            f"Error en el formateo del JSON: {e}. "
            f"Para más información, consulte la documentación: {DOCS_URL}"
        )

    try:
        with open(collection_json_path, "r", encoding="utf-8") as f:
            content = f.read()
            content.encode("utf-8").decode("utf-8")
    except UnicodeDecodeError as e:
        raise FormatError(
            f"Error en la codificación de caracteres: el archivo no está codificado en UTF-8. "
            f"Detalles: {e}. "
            f"Para más información, consulte la documentación: {DOCS_URL}"
        )
    except Exception as e:
        raise FormatError(
            f"Error al leer el archivo collection.json: {e}. "
            f"Para más información, consulte la documentación: {DOCS_URL}"
        )

    required_fields = ["id", "title", "description", "metadata", "items"]
    for field in required_fields:
        if field not in collection_data:
            raise FormatError(
                f"Campo requerido faltante: '{field}'. "
                f"Para más información, consulte la documentación: {DOCS_URL}"
            )

    if isinstance(collection_data.get("id"), str):
        collection_id = collection_data["id"]
        collection_id_pascal = _normalize_to_pascal_case(collection_id)

        if collection_id != collection_id.strip():
            raise FormatError(
                f"El campo 'id' no debe tener espacios al inicio o al final. "
                f"Valor actual: '{collection_id}'. "
                f"Para más información, consulte la documentación: {DOCS_URL}"
            )

        if collection_id != collection_id_pascal:
            logger.warning(
                f"El campo 'id' no está en PascalCase. "
                f"Valor actual: '{collection_id}'. "
                f"Se normalizará automáticamente a: '{collection_id_pascal}'. "
                f"Para más información, consulte la documentación: {DOCS_URL}"
            )

    text_fields = ["title", "description"]
    for field in text_fields:
        if field in collection_data:
            try:
                field_value = str(collection_data[field])
                field_value.encode("utf-8").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                raise FormatError(
                    f"Error en la codificación de caracteres en el campo '{field}': {e}. "
                    f"Para más información, consulte la documentación: {DOCS_URL}"
                )
