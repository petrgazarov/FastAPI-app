from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    database_url: str
    github_client_id: str
    github_client_secret: str
    internal_auth_token: str
    supertokens_api_key: str
    supertokens_connection_uri: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    # Workaround because Pyright does not work well with BaseSettings
    return Settings.parse_obj({})
