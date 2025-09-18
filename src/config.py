from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8082"
    abs_string: str = ""
    abs_container: str = "cog-test"
    auth_url: str = "/auth/token"
    username_auth: str = "admin"
    password_auth: str = "admin"
    token: str = ""
    main_file: str = "src/main.py"
    docs_dir: str = "docs"

    model_config = SettingsConfigDict(env_file=".env")

    def set_token(self, token: str):
        self.token = token


@lru_cache
def get_settings():
    return Settings()
