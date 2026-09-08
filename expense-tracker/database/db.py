import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if existing > 0:
            return

        password_hash = generate_password_hash("demo123")
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cur.lastrowid

        today = date.today()
        expenses = [
            (user_id, 450.00, "Food", today.replace(day=1).isoformat(), "Groceries - weekly shopping"),
            (user_id, 120.50, "Transport", today.replace(day=3).isoformat(), "Auto rickshaw fare"),
            (user_id, 1500.00, "Bills", today.replace(day=5).isoformat(), "Electricity bill"),
            (user_id, 800.00, "Health", today.replace(day=8).isoformat(), "Pharmacy - medicines"),
            (user_id, 600.00, "Entertainment", today.replace(day=10).isoformat(), "Movie tickets"),
            (user_id, 2200.00, "Shopping", today.replace(day=15).isoformat(), "New shoes"),
            (user_id, 300.00, "Other", today.replace(day=20).isoformat(), "Miscellaneous purchase"),
            (user_id, 550.75, "Food", today.replace(day=25).isoformat(), "Dinner with friends"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
