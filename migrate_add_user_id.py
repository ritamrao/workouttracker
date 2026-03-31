"""
One-time migration: adds user_id column to the sessions table
and assigns existing sessions to the admin user.

Run ONCE on an existing deployment before starting the updated app:
    python migrate_add_user_id.py
"""
import sqlite3
import os

db_path = os.environ.get('DB_PATH', 'gym.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add user_id column (nullable) if it doesn't already exist
existing = [row[1] for row in cursor.execute('PRAGMA table_info(sessions)').fetchall()]
if 'user_id' not in existing:
    cursor.execute('ALTER TABLE sessions ADD COLUMN user_id INTEGER REFERENCES users(id)')
    conn.commit()
    print("Added user_id column to sessions.")
else:
    print("user_id column already exists, skipping.")

# Assign orphaned sessions to the admin user
cursor.execute('SELECT id FROM users WHERE is_admin = 1 ORDER BY id LIMIT 1')
row = cursor.fetchone()
if row:
    admin_id = row[0]
    cursor.execute('UPDATE sessions SET user_id = ? WHERE user_id IS NULL', (admin_id,))
    conn.commit()
    print(f"Assigned {cursor.rowcount} orphaned sessions to admin (id={admin_id}).")
else:
    print("No admin user found. Start the app first to create the admin, then re-run this script.")

conn.close()
print("Migration complete.")
