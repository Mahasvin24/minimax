import sqlite3
import contextlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/db/memory.db")

@contextlib.contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Conversations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Facts table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Commit changes
        conn.commit()

# Saves message to db store
def save_message(session_id, role, content):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO conversations (session_id, role, content)
        VALUES (?, ?, ?)            
        """, (session_id, role, content))

        conn.commit()

# Loads all previous conversations in chronological order
def load_conversation(session_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(""" 
        SELECT role, content FROM conversations 
        WHERE session_id = ?
        ORDER BY timestamp
        """, (session_id,))

        rows = cursor.fetchall()

        return [{"role" : role, "content": content} for (role, content) in rows]
    
# Creates unique session id (based on exact date and time)
def new_session_id():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")