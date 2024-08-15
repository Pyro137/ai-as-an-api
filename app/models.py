import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from . import config



class SMSInference(Model):
    __keyspace__=config.ASTRA_DB_KEYSPACE
    uuid=columns.UUID(primary_key=True,default=uuid.uuid1)
    query=columns.Text()
    label=columns.Text()
    confidence=columns.Float()
    model_version = columns.Text(default='v1')