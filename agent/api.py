import ollama
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

# my imports
from storage import load_file, load_conversation

app = FastAPI()

MODEL = "gemma2:2b"
PERSOANLITY = Path("data/personality.md")
SYSTEM_PROMPT = load_file(PERSOANLITY)

# Load text from files
def load_file(path: Path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Path not found: {path}")

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
def chat(request: ChatRequest):
    messages = load_conversation(request.session_id)
    messages.append(request.message)
    res = ollama.chat(model=MODEL, messages=messages)
    return res

