from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    astra_client_id: str
    astra_client_secret: str
    aws_access_key_id: str
    aws_secret_access_key: str

# Manually create settings instance from environment variables


def get_settings():
    return Settings(
    astra_client_id=os.environ.get('ASTRA_CLIENT_ID'),
    astra_client_secret=os.environ.get('ASTRA_CLIENT_SECRET'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)