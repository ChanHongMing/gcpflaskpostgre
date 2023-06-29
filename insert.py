import psycopg2
import random
import string
from urllib.parse import urlparse

# Define the PostgreSQL database connection details
url = urlparse("postgres://zgirpxwy:cvDpInHGHTj0OovWFU5QJEkrX4Bv4X21@tiny.db.elephantsql.com/zgirpxwy")
conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Define a helper function to generate random strings for testing
def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Generate and insert three rows of randomly generated data into the users table
for i in range(3):
    username = random_string(8)
    password = random_string(12)
    insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');"
    cur.execute(insert_query)

# Commit the transaction and close the cursor and database connection
conn.commit()
cur.close()
conn.close()
