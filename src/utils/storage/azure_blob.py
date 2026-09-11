from urllib import parse

from azure.storage.blob import BlobServiceClient

from config import get_settings
from utils.logging_config import logger
from utils.storage.base import Storage


class AzureBlobStorage(Storage):

    def __init__(self):
        settings = get_settings()
        if not settings.abs_string:
            raise ValueError(
                "STORAGE_BACKEND=azure requires ABS_STRING to be set."
            )
        blob_service = BlobServiceClient.from_connection_string(
            settings.abs_string
        )
        self.container_client = blob_service.get_container_client(
            settings.abs_container
        )
        base = settings.asset_base_url or blob_service.url
        self.public_base = f"{base.rstrip('/')}/{settings.abs_container}"

    def upload_file(self, file_name, file_path):
        """
        Upload a blob to Azure Blob Storage
        """

        with open(file_path, "rb") as data:
            blob_client = self.container_client.upload_blob(
                file_name, data, overwrite=True, max_concurrency=4
            )
            return blob_client.url

    def build_object_url(self, file_name):
        return f"{self.public_base}/{file_name}"

    def remove_file(self, file_path):
        """
        Remove a blob from Azure Blob Storage
        """
        if file_path.startswith("https://"):
            parsed_url = parse.urlparse(file_path)
            file_path = parsed_url.path.lstrip("/")

        container_name = self.container_client.container_name

        if file_path.startswith(f"{container_name}/"):
            file_path = file_path[len(f"{container_name}/"):]

        blob_client = self.container_client.get_blob_client(file_path)

        if blob_client.exists():
            blob_client.delete_blob()
            logger.info(
                f"Successfully deleted {file_path} from Azure Blob Storage."
            )
        else:
            logger.warning(
                f"Blob {file_path} does not exist in Azure Blob Storage."
            )
