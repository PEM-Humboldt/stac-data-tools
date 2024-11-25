from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8082"
    abs_string: str = ""
    abs_container: str = "cog-test"
    auth_url: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
