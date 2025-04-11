import os
from shared.utils import singleton
from pydantic_settings import BaseSettings


@singleton
class Settings(BaseSettings):
    """Base settings for the application based on envrionment variables with default values"""

    mongoUri: str = os.getenv("MONGO_URI", "mongodb://admin:admin@mongodb:27017")
    mongoDatabase: str = os.getenv("MONGO_DATABASE", "concurrency_overview")

    fakerApiQuantity: int = int(os.getenv("FAKER_API_QUANTITY", "1000"))
    fakerApiUrl: str = os.getenv("FAKER_API_URL", "https://fakerapi.it/api/v1/users")

    @property
    def faker_api_url(self) -> str:
        return f"{self.fakerApiUrl}?_quantity={self.fakerApiQuantity}"
