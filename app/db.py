from app.config import ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET, ASTRA_DB_SECURE_BUNDLE_PATH, ASTRA_DB_KEYSPACE
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

def get_astra_session():
    cloud_config = {
        'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
    }
    auth_provider = PlainTextAuthProvider(
        ASTRA_DB_CLIENT_ID,
        ASTRA_DB_CLIENT_SECRET
    )
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect(ASTRA_DB_KEYSPACE)
    connection.register_connection('default', session=session, default=True)
    return session