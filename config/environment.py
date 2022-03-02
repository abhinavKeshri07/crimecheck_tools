from pydantic import BaseSettings
class Settings(BaseSettings):
    aws_access_key_id: str = "abcd"
    aws_secret_access_key: str = "abcd"
    aws_region:str = "ap-south-1"
    base_data_path : str
    callback_url: str
    crimecheck_api_key: str
    class Config:
        env_file = ".env"

settings = Settings()
