import sqlite3

# * Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# * 1. Create a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER,
        content TEXT,
        weight REAL,
        status TEXT
        )
    """
)

# * Close the connection when done
connection.close()
