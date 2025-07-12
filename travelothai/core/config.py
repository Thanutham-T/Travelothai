from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USE_MOCK: bool = False

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
