import os
import random
import sqlite3
from pathlib import Path
import base64
import json
import sys

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
import auth as auth_module  # noqa

DB_PATH = auth_module._db_path()

GREEN_DOT = (
    'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAGXRFW\nHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZZRCsIwEIXv0p0i7lV2\nY1pO5C4o6XHjB6l6GJJuCk0F6Gtw3Q0tEPpG4m3m+o2l1mQW8C0sS3kB\n5iQSYX2rY0p4t4p9r4dQ2m0iE+FJ0V7iCk4KQ6YmlO5f3wRk4eLw8H3Q\nG0OQ4Uo7u1jJf8I7x3vHkO1Y5p2XJ5nY3Cz6Gv4S6HcRr7N2G6uY8z5J\n7wE2UjH0bqLZ8hK2h0cV6xk1IYq4bqzvQyG8u0iS2dC0XyQdJ0vHh0jC\nG7uHjX0xI9cM+v5o8YtG4B3sTDK8sN8r6mXW5sGxqCqf6gWk5QWf7hJt\n9fU7c8mZy1kAAAAJcEhZcwAACxMAAAsTAQCanBgAAAANSURBVEhL7c0x\nAQAgEMKg+T8zIY0X4bA5pJpEb3wqv0IAA1tTj6wAAAABJRU5ErkJggg=='
)
RED_DOT = (
    'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAGXRFW\nHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZZRCsIwEIXv0p0i7lV2\nY1pO5C4o6XHjB6l6GJJuCk0F6Gtw3Q0tEPpG4m3m+o2l1mQW8C0sS3kB\n5iQSYX2rY0p4t4p9r4dQ2m0iE+FJ0V7iCk4KQ6YmlO5f3wRk4eLw8H3Q\nG0OQ4Uo7u1jJf8I7x3vHkO1Y5p2XJ5nY3Cz6Gv4S6HcRr7N2G6uY8z5J\n7wE2UjH0bqLZ8hK2h0cV6xk1IYq4bqzvQyG8u0iS2dC0XyQdJ0vHh0jC\nG7uHjX0xI9cM+v5o8YtG4B3sTDK8sN8r6mXW5sGxqCqf6gWk5QWf7hJt\n9fU7c8mZy1kAAAAJcEhZcwAACxMAAAsTAQCanBgAAAANSURBVEhL7c0x\nAQAgEMKg+T8zIY0X4bA5pJpEb3wqv0IAA1tTj6wAAAABJRU5ErkJggg=='
)

def tiny_data_url(color: str) -> str:
    # both strings are same PNG payload here for brevity
    b64 = GREEN_DOT if color == 'green' else RED_DOT
    return 'data:image/png;base64,' + b64.replace('\n', '')

SPECIES = [
    ("Kudzu", True),
    ("Japanese Knotweed", True),
    ("Garlic Mustard", True),
    ("Emerald Ash Borer", True),
    ("Spotted Lanternfly", True),
    ("English Ivy", True),
]

CENTER_LAT = 40.343094
CENTER_LNG = -74.651448


def jitter(val: float, radius: float = 0.01) -> float:
    return val + random.uniform(-radius, radius)


def ensure_reports_table(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            species TEXT,
            invasive INTEGER,
            summary TEXT,
            lat REAL,
            lng REAL,
            image_filename TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def seed(n: int = 15):
    auth_module.init_db()
    conn = sqlite3.connect(DB_PATH)
    ensure_reports_table(conn)
    cur = conn.cursor()
    for _ in range(n):
        sp, inv = random.choice(SPECIES)
        lat = jitter(CENTER_LAT, 0.01)
        lng = jitter(CENTER_LNG, 0.01)
        img = tiny_data_url('green' if inv else 'red')
        summary = f"Seeded report near Princeton for {sp}."
        cur.execute(
            """
            INSERT INTO reports (user_id, username, species, invasive, summary, lat, lng, image_filename, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (None, 'seed', sp, 1 if inv else 0, summary, lat, lng, img),
        )
    conn.commit()
    conn.close()
    print(f"Seeded {n} reports near Princeton into {DB_PATH}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Seed fake reports near Princeton into the database.')
    parser.add_argument('--count', '-c', type=int, default=15, help='Number of reports to insert')
    args = parser.parse_args()
    seed(args.count)
