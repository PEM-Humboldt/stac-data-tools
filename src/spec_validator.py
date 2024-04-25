from os import path, listdir
from json import load
from jsonschema import validate, FormatError


class SpecValidator:

    def __init__(self, folder, collection_name):
        self.folder = folder
        self.collection_name = collection_name

    def load_data(self):
        """
        Check if the collection folder exists and contains the collection file
        and load collection data
        """
        if not (
            path.exists(self.folder)
            and "collection.json" in listdir(self.folder)
        ):
            raise FileNotFoundError(
                f"El directorio {self.folder} no existe o "
                "no contiene el archivo collection.json."
            )

        with open("{}/collection.json".format(self.folder), "r") as f:
            self.data = load(f)
            self.raw_items = [item for item in self.data["items"]]

        return self.data, self.raw_items

    def validate_format(self):
        """
        Check if the collection.json file has the defined format
        """
        with open("spec/collection.json", "r") as f:
            schema = load(f)

        try:
            validate(instance=self.data, schema=schema)
        except Exception as e:
            raise FormatError(
                f"El archivo no cumple con el formato JSON. Detalles: {e}"
            )

    def validate_layers(self):
        """
        Check if the layer files exist
        """
        for item in self.raw_items:
            file_path = "{}/{}".format(
                self.folder, item["assets"]["input_file"]
            )
            if not path.exists(file_path):
                raise FileNotFoundError(
                    f"The file '{file_path}' does not exist."
                )
