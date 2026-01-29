import sqlite3
from passlib.context import CryptContext

# Use the same context as the backend
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Connect to the database
conn = sqlite3.connect('apps/backend/green_jobs.db')
cursor = conn.cursor()

# Check if user already exists
cursor.execute("SELECT * FROM users WHERE username = ?", ('testuser',))
existing_user = cursor.fetchone()

if existing_user:
    print("User 'testuser' already exists!")
else:
    # Hash the password using argon2
    hashed = pwd_context.hash("testpass123")

    # Insert the user
    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, ('testuser', 'test@example.com', hashed, 'job_seeker'))

    conn.commit()
    print("Test user 'testuser' created successfully!")
    print("Username: testuser")
    print("Password: testpass123")

# Verify
cursor.execute("SELECT username, email, role FROM users WHERE username = ?", ('testuser',))
user = cursor.fetchone()
if user:
    print(f"Verified: {user}")

conn.close()