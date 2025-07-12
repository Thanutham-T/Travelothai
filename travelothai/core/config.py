from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USE_MOCK: bool = False

    SECRET_KEY: str = "secret"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5 * 60  # 5 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    model_config = {"env_file": ".env", "validate_assignment": True, "extra": "allow"}

def get_settings() -> Settings:
    return Settings()
