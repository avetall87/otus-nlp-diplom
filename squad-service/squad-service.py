import os
from fastapi import FastAPI
from pydantic import BaseModel
from model import question_answerer
import uvicorn

app = FastAPI()

class SquadItem(BaseModel):
    context: str
    question: str

@app.get("/healthcheck")
def healthcheck():
    return 'Health - OK'

@app.post("/squad/")
def squad(item: SquadItem):
    return question_answerer(question=item.question, context=item.context)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(8085))