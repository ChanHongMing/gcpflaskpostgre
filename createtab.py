import psycopg2
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

# Define the CREATE TABLE statement
create_table_query = '''CREATE TABLE users
                        (ID SERIAL PRIMARY KEY,
                        USERNAME TEXT NOT NULL,
                        PASSWORD TEXT NOT NULL);'''

# Execute the CREATE TABLE statement
cur.execute(create_table_query)

# Commit the transaction and close the cursor and database connection
conn.commit()
cur.close()
conn.close()
