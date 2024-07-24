import sqlite3

# Connect to the SQLite database (or create it)
conn = sqlite3.connect("test_database.db")

# Create a cursor object
cursor = conn.cursor()

# Create a sample table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

# Insert sample data
cursor.execute("INSERT INTO users (name, age) VALUES (John Doe, 30)")
cursor.execute("INSERT INTO users (name, age) VALUES (Jane Smith, 25)")

# Commit the changes
conn.commit()

# Query the data
results = cursor.execute("SELECT * FROM users").fetchall()

# Save the results to query_results.txt
with open(query_results.txt, w) as f:
    for row in results:
        f.write(str(row) + n)

# Close the connection
conn.close()
