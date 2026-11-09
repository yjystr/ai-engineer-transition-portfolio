"""Phase 0 hello-world API for the AI Engineer transition plan.

Run locally:  uvicorn app.main:app --reload
Docs:          http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ai-transition-portfolio", version="0.1.0")


class Health(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=Health)
def health() -> Health:
    return Health(status="ok", service="ai-transition-portfolio")


@app.get("/")
def root() -> dict:
    return {"message": "hello world", "health": "/health", "docs": "/docs"}
