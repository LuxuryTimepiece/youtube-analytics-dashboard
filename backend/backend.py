from flask import Flask, jsonify, request
from flask_cors import CORS
from analysis import get_video_transcript, analyze_sentiment, extract_keywords
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize database with table creation
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

@app.route("/analyze/<video_id>", methods=["GET"])
def analyze_video(video_id):
    transcript = get_video_transcript(video_id)
    if not transcript:
        return jsonify({"error": "No transcript available"})
    
    sentiment = analyze_sentiment(transcript)
    keywords = extract_keywords(transcript)
    result = {
        "video_id": video_id,
        "transcript": transcript,
        "sentiment": sentiment,
        "keywords": ", ".join(keywords)  # String for SQLite
    }
    
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    # UPSERT: Insert or update if video_id exists
    cursor.execute("""
        INSERT OR REPLACE INTO analyses (video_id, transcript, sentiment, keywords)
        VALUES (?, ?, ?, ?)
    """, (result["video_id"], result["transcript"], result["sentiment"], result["keywords"]))
    conn.commit()
    conn.close()
    
    result["keywords"] = keywords  # List for frontend
    return jsonify(result)

if __name__ == "__main__":
    init_db()  # Ensure table exists on startup
    app.run(debug=True, host="0.0.0.0", port=5000)