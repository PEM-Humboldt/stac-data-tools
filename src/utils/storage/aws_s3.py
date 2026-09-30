import boto3
from botocore.config import Config

from config import get_settings
from utils.logging_config import logger
from utils.storage.base import Storage

COG_CONTENT_TYPE = "image/tiff; application=geotiff; profile=cloud-optimized"


class AWSS3Storage(Storage):

    def __init__(self):
        settings = get_settings()

        self.bucket = settings.s3_bucket
        if (
            not self.bucket
            or not settings.aws_access_key_id
            or not settings.aws_secret_access_key
        ):
            raise ValueError(
                "STORAGE_BACKEND=aws requires S3_BUCKET, AWS_ACCESS_KEY_ID and "
                "AWS_SECRET_ACCESS_KEY to be set."
            )
        region = settings.s3_region
        endpoint_url = settings.aws_endpoint_url or None

        self.public_base = f"https://{self.bucket}.s3.{region}.amazonaws.com"
        if settings.s3_public_url_base:
            self.public_base = settings.s3_public_url_base.rstrip("/")
        elif endpoint_url:
            self.public_base = f"{endpoint_url.rstrip('/')}/{self.bucket}"

        client_config = None
        if endpoint_url:
            client_config = Config(s3={"addressing_style": "path"})

        self.client = boto3.client(
            "s3",
            region_name=region,
            endpoint_url=endpoint_url,
            config=client_config,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            aws_session_token=settings.aws_session_token or None,
        )

    def upload_file(self, file_name, file_path):
        """
        Upload an object to AWS S3
        """
        self.client.upload_file(
            file_path,
            self.bucket,
            file_name,
            ExtraArgs={"ContentType": COG_CONTENT_TYPE},
        )

        try:
            self.client.head_object(Bucket=self.bucket, Key=file_name)
        except Exception as e:
            raise RuntimeError(
                f"There was an error while uploading {file_name} to "
                f"S3 bucket {self.bucket!r}: {e}"
            )

        return self.build_object_url(file_name)

    def build_object_url(self, file_name):
        return f"{self.public_base}/{file_name}"

    def remove_file(self, file_path):
        """
        Remove an object from AWS S3
        """
        prefix = f"{self.public_base}/"

        if file_path.startswith(prefix):
            file_path = file_path[len(prefix) :]

        response = self.client.list_objects_v2(
            Bucket=self.bucket, Prefix=file_path, MaxKeys=1
        )
        exists = any(
            obj["Key"] == file_path for obj in response.get("Contents", [])
        )

        if exists:
            self.client.delete_object(Bucket=self.bucket, Key=file_path)
            logger.info(f"Successfully deleted {file_path} from AWS S3.")
        else:
            logger.warning(f"Object {file_path} does not exist in AWS S3.")
