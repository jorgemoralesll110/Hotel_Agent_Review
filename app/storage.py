import sqlite3
import json
import time
from typing import Any, Dict, List, Optional, Tuple

DB_PATH = "../conversations.db"


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con


def init_db() -> None:
    with _conn() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL,
                title TEXT NOT NULL
            );
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                ts INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                meta_json TEXT,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            );
            """
        )
        con.commit()


def create_conversation(conversation_id: str, title: str) -> None:
    with _conn() as con:
        con.execute(
            "INSERT OR IGNORE INTO conversations(id, created_at, title) VALUES (?, ?, ?)",
            (conversation_id, int(time.time()), title),
        )
        con.commit()


def update_conversation_title(conversation_id: str, title: str) -> None:
    with _conn() as con:
        con.execute("UPDATE conversations SET title=? WHERE id=?", (title, conversation_id))
        con.commit()


def add_message(
    conversation_id: str,
    role: str,
    content: str,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    with _conn() as con:
        con.execute(
            "INSERT INTO messages(conversation_id, ts, role, content, meta_json) VALUES (?, ?, ?, ?, ?)",
            (
                conversation_id,
                int(time.time()),
                role,
                content,
                json.dumps(meta, ensure_ascii=False) if meta else None,
            ),
        )
        con.commit()


def list_conversations(limit: int = 200) -> List[Tuple[str, int, str]]:
    with _conn() as con:
        rows = con.execute(
            "SELECT id, created_at, title FROM conversations ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return rows


def load_conversation(conversation_id: str) -> List[Dict[str, Any]]:
    with _conn() as con:
        rows = con.execute(
            """
            SELECT ts, role, content, meta_json
            FROM messages
            WHERE conversation_id=?
            ORDER BY ts ASC, id ASC
            """,
            (conversation_id,),
        ).fetchall()

    out: List[Dict[str, Any]] = []
    for ts, role, content, meta_json in rows:
        out.append(
            {
                "ts": ts,
                "role": role,
                "content": content,
                "meta": json.loads(meta_json) if meta_json else None,
            }
        )
    return out


def delete_conversation(conversation_id: str) -> None:
    with _conn() as con:
        con.execute("DELETE FROM messages WHERE conversation_id=?", (conversation_id,))
        con.execute("DELETE FROM conversations WHERE id=?", (conversation_id,))
        con.commit()