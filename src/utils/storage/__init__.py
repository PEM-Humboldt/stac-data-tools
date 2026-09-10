from config import get_settings
from utils.storage.aws_s3 import AWSS3Storage
from utils.storage.azure_blob import AzureBlobStorage
from utils.storage.base import Storage


def get_storage() -> Storage:
    """
    Build the storage backend selected by STORAGE_BACKEND.
    """
    backend = get_settings().storage_backend.lower()

    if backend == "azure":
        return AzureBlobStorage()

    if backend == "aws":
        return AWSS3Storage()

    raise ValueError(
        f"Unsupported STORAGE_BACKEND {backend!r}. Use 'azure' or 'aws'."
    )
