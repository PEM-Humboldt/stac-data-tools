from azure.storage.blob import BlobServiceClient
from os import path


def upload_file(abs_config, folder_path, file_name):
    """
    Upload a blob to Azure Blob Storage
    """
    blob_service = BlobServiceClient.from_connection_string(
        abs_config.abs_string
    )
    container_client = blob_service.get_container_client(
        abs_config.abs_container
    )

    file_path = path.join(folder_path, file_name)
    blob_name = path.relpath(file_path, folder_path).replace("\\", "/")

    blob_client = container_client.get_blob_client(blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
