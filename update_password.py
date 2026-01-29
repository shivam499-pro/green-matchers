import sqlite3
from passlib.context import CryptContext

# Use the same context as the backend
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Connect to the database
conn = sqlite3.connect('apps/backend/green_jobs.db')
cursor = conn.cursor()

# Hash the correct password
hashed = pwd_context.hash("testpass123")

# Update the user
cursor.execute("""
    UPDATE users
    SET password = ?
    WHERE username = ?
""", (hashed, 'testuser'))

conn.commit()

# Verify
cursor.execute("SELECT username, password FROM users WHERE username = ?", ('testuser',))
user = cursor.fetchone()
if user:
    print(f"Updated user: {user[0]}")
    print(f"Password hash: {user[1][:50]}...")

conn.close()
print("Password updated successfully!")