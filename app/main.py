
import os
import pathlib
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from cassandra.query import SimpleStatement
from cassandra.cqlengine.management import sync_table

from . import (
    config,
    db, 
    models,
    ml,
    schema
)

app=FastAPI()


BASE_DIR=pathlib.Path(__file__).resolve().parent
MODEL_DIR=BASE_DIR/"models"
SMS_SPAM_MODEL_DIR=MODEL_DIR/"spam-sms"
MODEL_PATH=pathlib.Path("models\spam-sms\spam-model.h5")
METADATA_PATH=pathlib.Path("models\spam-sms\spam-classifer-metadata.json")
TOKENIZER_PATH=pathlib.Path("models\spam-sms\spam-classifer-tokenizer.json")

AI_MODEL=None
DB_SESSION=None
SMSInference=models.SMSInference

@app.on_event("startup")
def on_startup():
    global AI_MODEL, DB_SESSION
    AI_MODEL = ml.AIModel(
        model_path= MODEL_PATH,
        tokenizer_path = TOKENIZER_PATH,
        metadata_path = METADATA_PATH
    )
    DB_SESSION = db.get_astra_session()
    sync_table(SMSInference)
    

@app.get("/")
def read_index(q:Optional[str] = None):
    query=q or "hello world"
    preds=AI_MODEL.predict_text(query)
    top=preds.get("top")
    data={"query":query,**top}
    obj=SMSInference.objects.create(**data)
    
    return obj

@app.post("/")
def create_inference(query: schema.Query):
    global AI_MODEL
    preds_dict = AI_MODEL.predict_text(query.q)
    top = preds_dict.get('top')  # {label: , conf}
    data = {"query": query.q, **top}
    obj = SMSInference.objects.create(**data)
    return obj


@app.get("/inferences") # /?q=this is awesome
def list_inference():
    q = SMSInference.objects.all()
    print(q)
    return list(q)


@app.get("/inferences/{my_uuid}") # /?q=this is awesome
def read_inference(my_uuid):
    obj = SMSInference.objects.get(uuid=my_uuid)
    return obj


def fetch_rows(
        stmt: SimpleStatement, 
        fetch_size: int = 25, 
        session=None):
    stmt.fetch_size = fetch_size
    result_set = session.execute(stmt)
    has_pages = result_set.has_more_pages
    yield "uuid,label,confidence,query,version\n"
    while True:
        for row in result_set.current_rows:
            yield f"{row['uuid']},{row['label']},{row['confidence']},{row['query']},{row['model_version']}\n"
        if not has_pages:
            break
        result_set = session.execute(stmt, paging_state=result_set.paging_state)
        has_pages = result_set.has_more_pages


@app.get("/dataset")
def export_inferences():
    global DB_SESSION
    cql_query = "SELECT * FROM astra_db_keyspace.smsinference LIMIT 10000"
    statement = SimpleStatement(cql_query)
    return StreamingResponse(fetch_rows(statement, 25, DB_SESSION))
