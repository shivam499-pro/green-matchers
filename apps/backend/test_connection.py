import mariadb

try:
    conn = mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="greenmatchers2025"  # Fixed to match your .env file
    )
    print("Connection successful!")
    conn.close()
except mariadb.Error as e:
    print(f"Connection failed: {e}")
