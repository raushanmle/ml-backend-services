from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_PORT: int = Field(None, validation_alias="DATABASE_PORT")
    POSTGRES_PASSWORD: str = Field(None, validation_alias="POSTGRES_PASSWORD")
    POSTGRES_USER: str = Field(None, validation_alias="POSTGRES_USER")
    POSTGRES_DB: str = Field(None, validation_alias="POSTGRES_DB")
    POSTGRES_HOSTNAME: str = Field(None, validation_alias="POSTGRES_HOSTNAME")
    COMPOSE_PROJECT_NAME: str = Field(
        None, validation_alias="COMPOSE_PROJECT_NAME")

    class Config:
        env_file = '.env'


settings = Settings()

# Construct the DATABASE_URL
DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
)
