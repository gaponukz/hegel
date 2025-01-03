import typing

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    app_name: str = "Dialectic API"
    neo4j_uri: str
    neo4j_database: str
    neo4j_user: str
    neo4j_password: str
    token: typing.Optional[str] = None


config = AppConfig()  # type: ignore
