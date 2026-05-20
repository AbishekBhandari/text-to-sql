from fastapi import FastAPI
from .agent import run_agent

app = FastAPI()


@app.post("/agent/sql")
def agent_sql(payload: dict):

    question = payload["question"]

    return run_agent(question)