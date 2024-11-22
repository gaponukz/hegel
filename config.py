from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    app_name: str = "Dialectic API"
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str


config = AppConfig()  # type: ignore