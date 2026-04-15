import ollama
from ollama import generate

MODEL = "gemma2:2b"

response = generate(MODEL, "What is 6 + 6?")

print(response["response"])