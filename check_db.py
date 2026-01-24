import sqlite3

conn = sqlite3.connect('Backend/green_jobs.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables in SQLite DB:', tables)

# Check if careers and jobs tables exist
if ('careers',) in tables:
    cursor.execute("SELECT COUNT(*) FROM careers")
    careers_count = cursor.fetchone()[0]
    print(f"Careers table has {careers_count} records")
else:
    print("Careers table does not exist")

if ('jobs',) in tables:
    cursor.execute("SELECT COUNT(*) FROM jobs")
    jobs_count = cursor.fetchone()[0]
    print(f"Jobs table has {jobs_count} records")
else:
    print("Jobs table does not exist")

conn.close()