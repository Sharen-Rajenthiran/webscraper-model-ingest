from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBEDDINGS_MODEL: str = config("EMBEDDINGS_MODEL") 
    PORT: int = config("PORT")
    ZUS_DRINKWARE_URL : str = config("ZUS_DRINKWARE_URL")
    
    class Config:
        case_sensitive = True

settings = Settings()
