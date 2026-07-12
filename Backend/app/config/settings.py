from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    news_api_key : str
    news_provider:str
    news_base_url:str
    hf_token:str

    class Config:
        env_file = ".env"

settings = Settings()
