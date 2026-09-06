from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://gold_user:gold_pass@localhost:5432/gold_intelligence"

    goldapi_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
