import os
import pathlib
from typing import Optional
from fastapi import FastAPI
from . import ml
from .config import get_settings

app = FastAPI()
settings = get_settings()

BASE_DIR = pathlib.Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR.parent / "models"
SMS_SPAM_MODEL_DIR = MODEL_DIR / "spam-sms"
MODEL_PATH = SMS_SPAM_MODEL_DIR / "spam-model.h5"
TOKENIZER_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-tokenizer.json"
METADATA_PATH = SMS_SPAM_MODEL_DIR / "spam-classifer-metadata.json"

AI_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL
    AI_MODEL = ml.AIModel(
        model_path=MODEL_PATH,
        tokenizer_path=TOKENIZER_PATH,
        metadata_path=METADATA_PATH
    )

@app.get("/")
def read_index(q: Optional[str] = None):
    query = q or "Hello world"
    predictions = AI_MODEL.predict_text(query=query)
    return {"predictions": predictions,"db_client_id":settings.aws_access_key_id}