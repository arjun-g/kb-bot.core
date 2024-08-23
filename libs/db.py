import os
from peewee import MySQLDatabase, Model, CharField, TextField, FloatField, SQL
from tidb_vector.peewee import VectorField

tidb = MySQLDatabase(
    database=os.environ.get('TIDB_DATABASE', 'test'),
    user=os.environ.get('TIDB_USERNAME', 'root'),
    password=os.environ.get('TIDB_PASSWORD', ''),
    host=os.environ.get('TIDB_HOST', 'localhost'),
    port=int(os.environ.get('TIDB_PORT', '4000')),
    ssl_verify_cert = True,
    ssl_verify_identity = True
)

class KB(Model):
    class Meta:
        database = tidb
        table_name = 'kb'
    
    id = CharField(primary_key=True)
    title = TextField()
    content = TextField()
    ref = TextField()
    embedding = VectorField(768, constraints=[SQL("COMMENT 'hnsw(distance=cosine)'")])

class TiDBProvider():
    def connect(self):
        tidb.connect()
        if(not tidb.table_exists('kb')):
            tidb.create_tables([KB])
            
    def disconnect(self):
        tidb.close()
        
    def insert(self, kb):
        print("INSERT KB")
        try:
            KB.create(
                id=kb['id'],
                title=kb['title'],
                content=kb['content'],
                ref=kb['ref'],
                embedding=kb['embedding']
            )
        except Exception as e: print(e)
        
