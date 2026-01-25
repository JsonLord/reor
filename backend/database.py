import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

embedding_function = get_registry().get("sentence-transformers").create()

class ReorTableModel(LanceModel):
    text: str = embedding_function.SourceField()
    vector: Vector(embedding_function.ndims()) = embedding_function.VectorField()
    notepath: str

from contextlib import contextmanager

class LanceDBTableWrapper:
    def __init__(self, db_path: str, table_name: str):
        self.db_path = db_path
        self.table_name = table_name
        self.db = None
        self.table = None

    def __enter__(self):
        self.db = lancedb.connect(self.db_path)
        if self.table_name not in self.db.list_tables():
            self.db.create_table(self.table_name, schema=ReorTableModel)
        self.table = self.db.open_table(self.table_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def search(self, query: str, limit: int = 5):
        results = self.table.search(query).limit(limit).to_pydantic(ReorTableModel)
        return [result.text for result in results]

@contextmanager
def get_db():
    db = LanceDBTableWrapper("data/lancedb", "reor_table")
    try:
        with db as conn:
            yield conn
    finally:
        pass
