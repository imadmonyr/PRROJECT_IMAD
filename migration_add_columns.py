"""
LUXEDRIVE — Migration Script
Run this ONCE to add the new columns to your existing database.

Usage (from your project folder, with venv activated):
    python migration_add_columns.py

It is safe to run multiple times — uses ALTER TABLE ... ADD COLUMN which
fails silently if the column already exists.
"""

import os
import sqlite3

# Resolve path to database.db (same folder as this script)
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'database.db')

if not os.path.exists(DB_PATH):
    # Try one level up (if you put this script in a subdirectory)
    DB_PATH = os.path.join(os.path.dirname(BASE), 'database.db')

print(f"Database: {DB_PATH}")

db = sqlite3.connect(DB_PATH)
cur = db.cursor()

migrations = [
    # Add adresse column to client table
    ("client",      "adresse", "ALTER TABLE client      ADD COLUMN adresse TEXT"),
    # Add email column to fournisseur table
    ("fournisseur", "email",   "ALTER TABLE fournisseur ADD COLUMN email   TEXT"),
]

for table, col, sql in migrations:
    try:
        cur.execute(sql)
        db.commit()
        print(f"  ✓ Added column `{col}` to table `{table}`")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"  — Column `{col}` already exists in `{table}` (skipped)")
        else:
            print(f"  ✗ Error on `{table}.{col}`: {e}")

db.close()
print("\nDone. You can now restart the app (python app.py).")
