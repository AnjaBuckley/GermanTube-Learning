import sqlite3
import json
import os
from datetime import datetime

# Database file path
DB_PATH = "germanlearning.db"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create quiz_results table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        video_id TEXT,
        score INTEGER,
        total_questions INTEGER,
        results TEXT,
        timestamp TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def save_quiz_result(video_id, score, total_questions, results):
    """Save quiz results to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # For now, we'll use a placeholder user_id
    # In a real app, you'd have user authentication
    user_id = "default_user"
    
    # Convert results to JSON string
    results_json = json.dumps(results)
    
    # Get current timestamp
    timestamp = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO quiz_results (user_id, video_id, score, total_questions, results, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, video_id, score, total_questions, results_json, timestamp)
    )
    
    conn.commit()
    conn.close()

def get_user_history(user_id="default_user"):
    """Get quiz history for a user."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,)
    )
    
    rows = cursor.fetchall()
    
    # Convert rows to dictionaries
    history = []
    for row in rows:
        item = dict(row)
        item["results"] = json.loads(item["results"])
        history.append(item)
    
    conn.close()
    return history 