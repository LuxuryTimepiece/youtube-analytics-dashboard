# YouTube Analytics Dashboard

A web app to fetch and analyze YouTube video transcripts, providing sentiment analysis and keyword extraction.

## Features
- Extracts transcripts using `yt-dlp`.
- Sentiment analysis with TextBlob.
- Keyword extraction with spaCy.
- Duplicate-free transcript processing.
- SQLite storage for analysis history.

## Setup
### Backend (Python)
1. `cd backend`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Download spaCy model: `python3 -m spacy download en_core_web_sm`
4. Add `cookies.txt` (YouTube login export) to `backend/`
5. Run: `python3 backend.py`

### Frontend (Node.js)
1. `cd frontend`
2. Install dependencies: `npm install`
3. Run: `npm start`

## Usage
- Open `http://localhost:3000`.
- Enter a YouTube video ID (e.g., `dQw4w9WgXcQ`).
- View transcript, sentiment, and keywords.

## Tech Stack
- **Backend**: Flask, Python, SQLite, yt-dlp, TextBlob, spaCy.
- **Frontend**: React, Node.js, Axios.

## Notes
- Requires YouTube cookies for transcript access.
- Handles duplicate text from `.vtt` files effectively.

## Demo
[Link to video/screenshot if hosted later]

## License
MIT