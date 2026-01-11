from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    AI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
