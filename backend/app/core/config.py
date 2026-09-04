from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://gold_user:gold_pass@localhost:5432/gold_intelligence"

    # کلیدهای API — بعدا با .env پر می‌شن، هیچ‌وقت hardcode نشن
    goldapi_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
