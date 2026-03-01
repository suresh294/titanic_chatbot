from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .agent import ask_agent

app = FastAPI(
    title="Titanic AI Chatbot API",
    description="AI chatbot for analyzing the Titanic dataset.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Titanic AI Chatbot API is running 🚢"}

@app.post("/ask")
async def ask(query: Query):
    answer = ask_agent(query.question)
    return {
        "question": query.question,
        "answer": answer
    }