import sqlite3

# * Make the connection
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# * 1. Create a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipment (
        id INTEGER PRIMARY KEY,
        content TEXT,
        weight REAL,
        status TEXT
        )
    """
)

# cursor.execute("DROP TABLE shipment")
# connection.commit()

# * 2. Add shipment data
cursor.execute(
    """
    INSERT INTO shipment
    VALUES  (12701, 'metal gears', 12, 'placed')
    """
)
connection.commit()

# * 3. Read a shipment by id
cursor.execute(
    """
        SELECT * FROM shipment 
        WHERE content = 'palm trees'
    """
)
result = cursor.fetchone()
print(result)

# * 4. Delete a shipment by id
# cursor.execute(
#     """
#         DELETE FROM shipment
#         WHERE id = 12703
#     """
# )
# connection.commit()

# * Close the connection when done
connection.close()
