from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8082"

    # Storage backend selection: "azure" or "s3"
    storage_backend: str = "azure"

    # --- Azure Blob Storage ---
    abs_string: str = ""
    abs_container: str = "cog-test"
    asset_base_url: str = "https://staccatalog.blob.core.windows.net"

    # --- AWS S3 ---
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    # Override the S3 endpoint (e.g. LocalStack: http://host:4566).
    aws_endpoint_url: str = ""
    # Optional public base URL for asset hrefs (CloudFront / custom domain).
    # When empty, the virtual-hosted S3 URL is used.
    s3_public_url_base: str = ""

    auth_url: str = "/auth/token"
    username_auth: str = "admin"
    password_auth: str = "admin"
    token: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def set_token(self, token: str):
        self.token = token


@lru_cache
def get_settings():
    return Settings()
