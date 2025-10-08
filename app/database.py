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

# * 2. Add shipment data
cursor.execute(
    """
    INSERT INTO shipment
    VALUES  (12702, 'baslat', 18.7, 'in_transit')   
    """
)
connection.commit()

# * Close the connection when done
connection.close()
