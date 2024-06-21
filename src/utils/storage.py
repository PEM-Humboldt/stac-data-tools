from azure.storage.blob import BlobServiceClient
from config import get_settings


class Storage:

    def __init__(self):
        settings = get_settings()
        blob_service = BlobServiceClient.from_connection_string(
            settings.abs_string
        )
        self.container_client = blob_service.get_container_client(
            settings.abs_container
        )

    def upload_file(self, file_name, file_path):
        """
        Upload a blob to Azure Blob Storage
        """

        with open(file_path, "rb") as data:
            blob_client = self.container_client.upload_blob(
                file_name, data, overwrite=True
            )
            return blob_client.url

    def remove_file(self, file_path):
        """
        Remove a blob from Azure Blob Storage
        """
        blob_client = self.container_client.get_blob_client(file_path)
        if blob_client.exists():
            blob_client.delete_blob()
