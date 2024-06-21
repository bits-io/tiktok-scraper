from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    WEBDRIVER_DIR: str

    class Config:
        env_file = ".env"

settings = Settings()
