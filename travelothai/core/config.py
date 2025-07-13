from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USE_MOCK: bool = False

    SQLDB_URL: str
    SECRET_KEY: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    model_config = {"env_file": ".env", "validate_assignment": True, "extra": "allow"}

def get_settings() -> Settings:
    return Settings()
