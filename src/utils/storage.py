from abc import ABC, abstractmethod
from urllib import parse

from config import get_settings
from utils.logging_config import logger

COG_CONTENT_TYPE = "image/tiff; application=geotiff; profile=cloud-optimized"


class Storage(ABC):
    """
    Abstract storage backend. Each cloud provider is implemented as a
    concrete subclass..
    """

    @abstractmethod
    def upload_file(self, file_name: str, file_path: str) -> str:
        """
        Upload a local file under the key ``file_name`` and return the
        public href that will be stored as the STAC asset href.
        """

    @abstractmethod
    def remove_file(self, file_path: str) -> None:
        """
        Remove an object given the href exactly as it was stored in the
        STAC asset (a full URL) or a bare key.
        """

    @abstractmethod
    def build_object_url(self, file_name: str) -> str:
        """
        Build the public href for a key without uploading anything.
        """


class AzureBlobStorage(Storage):

    def __init__(self):
        from azure.storage.blob import BlobServiceClient

        settings = get_settings()
        self.blob_service = BlobServiceClient.from_connection_string(
            settings.abs_string
        )
        self.container_name = settings.abs_container
        self.container_client = self.blob_service.get_container_client(
            self.container_name
        )
        self._public_base = settings.asset_base_url.rstrip(
            "/"
        ) or self.blob_service.url.rstrip("/")

    def upload_file(self, file_name, file_path):
        """
        Upload a blob to Azure Blob Storage.
        """
        with open(file_path, "rb") as data:
            blob_client = self.container_client.upload_blob(
                file_name, data, overwrite=True, max_concurrency=4
            )
            return blob_client.url

    def build_object_url(self, file_name):
        return f"{self._public_base}/{self.container_name}/{file_name}"

    def remove_file(self, file_path):
        """
        Remove a blob from Azure Blob Storage.
        """
        if file_path.startswith("https://"):
            parsed_url = parse.urlparse(file_path)
            file_path = parsed_url.path.lstrip("/")

        container_name = self.container_client.container_name

        if file_path.startswith(f"{container_name}/"):
            file_path = file_path[len(f"{container_name}/") :]

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


class S3Storage(Storage):

    def __init__(self):
        import boto3
        from botocore.config import Config

        settings = get_settings()
        self.bucket = settings.s3_bucket
        self.region = settings.s3_region
        endpoint_url = settings.aws_endpoint_url or None

        client_config = None
        if endpoint_url:
            client_config = Config(s3={"addressing_style": "path"})

        # Pass explicit credentials only when provided in the config;
        # otherwise let boto3 resolve them (env vars, shared config, IAM
        # role).
        creds = {}
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            creds["aws_access_key_id"] = settings.aws_access_key_id
            creds["aws_secret_access_key"] = settings.aws_secret_access_key
            if settings.aws_session_token:
                creds["aws_session_token"] = settings.aws_session_token

        self.client = boto3.client(
            "s3",
            region_name=self.region or None,
            endpoint_url=endpoint_url,
            config=client_config,
            **creds,
        )

        if settings.s3_public_url_base:
            self._public_base = settings.s3_public_url_base.rstrip("/")
        elif endpoint_url:
            self._public_base = f"{endpoint_url.rstrip('/')}/{self.bucket}"
        else:
            self._public_base = (
                f"https://{self.bucket}.s3.{self.region}.amazonaws.com"
            )

    def upload_file(self, file_name, file_path):
        """
        Upload an object to AWS S3.
        """
        self.client.upload_file(
            file_path,
            self.bucket,
            file_name,
            ExtraArgs={"ContentType": COG_CONTENT_TYPE},
        )
        return self.build_object_url(file_name)

    def build_object_url(self, file_name):
        return f"{self._public_base}/{file_name}"

    def remove_file(self, file_path):
        """
        Remove an object from AWS S3.
        """
        key = self._key_from_href(file_path)

        response = self.client.list_objects_v2(
            Bucket=self.bucket, Prefix=key, MaxKeys=1
        )
        exists = any(obj["Key"] == key for obj in response.get("Contents", []))

        if exists:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"Successfully deleted {key} from AWS S3.")
        else:
            logger.warning(f"Object {key} does not exist in AWS S3.")

    def _key_from_href(self, file_path):
        """
        Derive the object key from whatever was stored as the asset href.
        Tolerates full URLs (virtual-hosted, path-style, LocalStack),
        ``s3://bucket/key`` and bare keys.
        """
        if file_path.startswith(f"{self._public_base}/"):
            return file_path[len(self._public_base) + 1 :]

        if file_path.startswith("s3://"):
            without_scheme = file_path[len("s3://") :]
            _, _, key = without_scheme.partition("/")
            return key

        if file_path.startswith(("http://", "https://")):
            path = parse.urlparse(file_path).path.lstrip("/")
            # path-style URLs carry the bucket as the first segment
            if path.startswith(f"{self.bucket}/"):
                path = path[len(self.bucket) + 1 :]
            return path

        return file_path.lstrip("/")


def get_storage() -> Storage:
    """
    Build the storage backend selected by STORAGE_BACKEND.
    """
    settings = get_settings()
    backend = settings.storage_backend.lower()

    if backend == "azure":
        if not settings.abs_string:
            raise ValueError(
                "STORAGE_BACKEND=azure requires ABS_STRING to be set."
            )
        return AzureBlobStorage()

    if backend == "s3":
        if not settings.s3_bucket:
            raise ValueError(
                "STORAGE_BACKEND=s3 requires S3_BUCKET to be set."
            )
        return S3Storage()

    raise ValueError(
        f"Unsupported STORAGE_BACKEND {backend!r}. Use 'azure' or 's3'."
    )
