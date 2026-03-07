from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ADMIN:str
    ADMIN_PASSWORD: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENCRYPTION_KEY: str

    class Config:
        env_file = '.env.example'

settings = Settings()