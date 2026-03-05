import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_name: str = "Api-service"
    db_user: str | None = os.getenv("DB_USER")
    db_password: str | None = os.getenv("DB_PASSWORD")
    db_host: str | None = os.getenv("DB_HOST")
    db_name: str | None = os.getenv("DB_NAME")
    jsonplaceholder_base_url: str = os.getenv(
        "JSONPLACEHOLDER_BASE_URL",
        "https://jsonplaceholder.typicode.com",
    ).rstrip("/")
    api_key_pepper: str = os.getenv("API_KEY_PEPPER", "change-me-in-env")

    @property
    def database_url(self) -> str:
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}/{self.db_name}"
        )


settings = Settings()
