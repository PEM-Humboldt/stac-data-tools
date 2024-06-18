from azure.storage.blob import BlobServiceClient
from config import get_settings


def config():
    """
    Get the values of env and create container client
    """
    # TODO: Considerar si este script deberia ser una clase
    settings = get_settings()

    blob_service = BlobServiceClient.from_connection_string(
        settings.abs_string
    )
    container_client = blob_service.get_container_client(
        settings.abs_container
    )

    return container_client


def upload_file(file_name, file_path):
    """
    Upload a blob to Azure Blob Storage
    """
    container_client = config()

    with open(file_path, "rb") as data:
        blob_client = container_client.upload_blob(
            file_name, data, overwrite=True
        )
        return blob_client.url


def remove_file(file_path):
    """
    Remove a blob from Azure Blob Storage
    """
    container_client = config()

    blob_client = container_client.get_blob_client(file_path)
    blob_client.delete_blob()
