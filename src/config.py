from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8082"

    storage_backend: Literal["azure", "aws"] = "azure"

    abs_string: str = ""
    abs_container: str = "cog-test"
    asset_base_url: str = "https://staccatalog.blob.core.windows.net"

    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    aws_endpoint_url: str = ""
    s3_public_url_base: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""

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
