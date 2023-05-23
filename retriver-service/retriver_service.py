import os
from fastapi import FastAPI
from model.bert_model import find_similarity_documents
import uvicorn

min_similarity_weight = 60.0

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return 'Health - OK'

@app.get("/search-doc/{query}")
def get_doc(query: str):
    similarities = []

    for similarity in find_similarity_documents(query):
        if similarity['weight'] >= min_similarity_weight:
            similarities.append(similarity)

    return similarities


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(8080))