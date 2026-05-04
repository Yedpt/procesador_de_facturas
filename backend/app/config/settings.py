 # variables entorno
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #APP

    app_env: str = "local"

    #database   
    database_url: str 

    #Vertex AI
    google_application_credentials: str
    gcp_project_id: str
    gcp_location: str = "europe-west1"
    gemini_model: str = "gemini-1.5-pro"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()