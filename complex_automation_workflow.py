import requests
import sqlite3

# Step 1: Fetch data from API
api_url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(api_url)
data = response.json()

# Step 2: Connect to SQLite database
conn = sqlite3.connect("users_data.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
"""
)

# Insert data into the database
for user in data:
    cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                   (user["id"], user["name"], user["email"]))

conn.commit()

# Step 3: Query the data
results = cursor.execute("SELECT name FROM users").fetchall()

# Step 4: Save the results to a text file
with open("user_names.txt", "w") as f:
    for row in results:
        f.write(row[0] + "
")

# Close the database connection
conn.close()

