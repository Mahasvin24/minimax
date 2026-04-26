import ollama
from pathlib import Path

# my imports
from storage import init_db, new_session_id, save_message

# Load text from files
def load_file(path: Path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Path not found: {path}")

MODEL = "gemma2:2b"
PERSOANLITY = Path("data/personality.md")
SYSTEM_PROMPT = load_file(PERSOANLITY)

init_db()
session_id = new_session_id()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# messages += load_conversation("2026-04-17_01-59-34")

print("Starting conversation with Max. Use /bye to exit...\n")

while True:
    user_message = input("Mahasvin: ").strip()
    print()

    # try again for empty input
    if not user_message:
        continue

    # end convo on bye
    if user_message.lower() == "/bye":
        print("Conversation ended.")
        break

    messages.append({"role": "user", "content": user_message})
    save_message(session_id, role="user", content=user_message)

    print("Max: ", end="", flush=True)

    agent_message = ""

    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True):
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        agent_message += token

    messages.append({"role": "assistant", "content": agent_message})
    save_message(session_id, role="assistant", content=agent_message)

    print()
    



