from fastapi import FastAPI
from pydantic import BaseModel
from . import llm, database

app = FastAPI()

from fastapi import Depends

class EmbeddingsRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    question: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/embeddings")
def create_embedding(request: EmbeddingsRequest):
    embedding = llm.get_embedding(request.text)
    return {"embedding": embedding}

@app.post("/api/query")
def answer_query(request: QueryRequest, db: database.LanceDBTableWrapper = Depends(database.get_db)):
    context = db.search(request.question)
    answer = llm.answer_question(request.question, context)
    return {"answer": answer}

@app.get("/api/search")
def search(query: str, db: database.LanceDBTableWrapper = Depends(database.get_db)):
    results = db.search(query)
    return {"results": results}
