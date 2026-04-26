import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    load_dotenv()
    DATABASE_URL: str = os.getenv('DATABASE_URL'),
    ECHO: bool = os.getenv('ECHO'),
    POOL_SIZE: int = os.getenv('POOL_SIZE'),
    MAX_OVERFLOW: int = os.getenv('MAX_OVERFLOW'),
    POOL_PRE_PING: bool = os.getenv('POOL_PRE_PING'),
    SECRET_KEY: str = os.getenv('SECRET_KEY'),
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'),
    ALGORITHM: str = os.getenv('ALGORITHM'),

    class Config:
        env_file='.env'
        extra='allow'


settings = Settings()
