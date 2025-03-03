import subprocess
import os
import glob
from textblob import TextBlob
import spacy
import re
import time

nlp = spacy.load("en_core_web_sm")

def get_video_transcript(video_id):
    for file in glob.glob("*.vtt") + glob.glob("*.srt"):
        os.remove(file)
    
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--cookies", "cookies.txt",
        f"https://youtu.be/{video_id}"
    ]
    for attempt in range(3):
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subtitle_files = glob.glob(f"*{video_id}*.en.vtt")
            print(f"Subtitle files found: {subtitle_files}")
            if not subtitle_files:
                print("No subtitle files downloaded.")
                return None
            
            with open(subtitle_files[0], "r") as f:
                lines = f.readlines()
            
            if not lines:
                print(f"Empty .vtt file for {video_id}")
                os.remove(subtitle_files[0])
                return None
            
            # Build transcript, deduplicating overlaps
            full_text = ""
            for line in lines:
                line = line.strip()
                if not line or line.startswith("WEBVTT") or line.startswith("NOTE") or "-->" in line:
                    continue
                # Remove all tags and closed captions
                line = re.sub(r'<[^>]+>', '', line)
                line = re.sub(r'\[(Music|Applause|Laughter|Cheering)\]', '', line, flags=re.IGNORECASE)
                if not line:
                    continue
                new_text = line.strip()
                if new_text and new_text not in full_text:
                    # Check for overlap and append only new content
                    overlap_idx = full_text.find(new_text)
                    if overlap_idx == -1:  # No overlap, append full text
                        full_text += " " + new_text if full_text else new_text
                    elif overlap_idx > 0:  # Partial overlap, trim and append
                        non_overlap = new_text[len(full_text[overlap_idx:]):].strip()
                        if non_overlap:
                            full_text += " " + non_overlap
            
            os.remove(subtitle_files[0])
            if not full_text:
                print(f"No valid transcript text extracted for {video_id}")
                return None
            print(f"Transcript extracted: {full_text[:100]}...")  # Log first 100 chars
            return full_text.strip()
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed: {e.stderr.decode()}")
            if "Sign in to confirm" in e.stderr.decode() or "HTTP Error 400" in e.stderr.decode():
                time.sleep(5)
            else:
                return None
    return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

def extract_keywords(text, top_n=5):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and token.text not in [">", "<c"]]
    from collections import Counter
    return [word for word, count in Counter(keywords).most_common(top_n)]