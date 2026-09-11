from config import get_settings
from utils.storage.aws_s3 import AWSS3Storage
from utils.storage.azure_blob import AzureBlobStorage
from utils.storage.base import Storage


def get_storage() -> Storage:
    """
    Build the storage backend selected by STORAGE_BACKEND.
    """
    if get_settings().storage_backend == "azure":
        return AzureBlobStorage()
    return AWSS3Storage()
