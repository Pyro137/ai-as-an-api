import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
# AstraDB Configuration
ASTRA_DB_CLIENT_ID = os.getenv('ASTRA_DB_CLIENT_ID')
ASTRA_DB_CLIENT_SECRET = os.getenv('ASTRA_DB_CLIENT_SECRET')
ASTRA_DB_SECURE_BUNDLE_PATH = os.getenv('ASTRA_DB_SECURE_BUNDLE_PATH')
ASTRA_DB_KEYSPACE = os.getenv('ASTRA_DB_KEYSPACE')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
REGION_NAME = os.getenv('REGION_NAME')

