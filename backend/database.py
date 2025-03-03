import sqlite3

def init_db():
    conn = sqlite3.connect("history.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            video_id TEXT PRIMARY KEY,
            transcript TEXT,
            sentiment TEXT,
            keywords TEXT
        )
    """)
    conn.close()

if __name__ == "__main__":
    init_db()