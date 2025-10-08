import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any


class Database:
    def __init__(self):
        # * Make the connection with db
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        #  * Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        # * Create table if not exits
        self.create_table()

    def create_table(self):
        # * 1. Create a table
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
                )
            """,
        )

    def create(self, shipment: ShipmentCreate) -> int:
        # * Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        self.cur.execute(
            """
            INSERT INTO shipment
            VALUES  (:id, :content, :weight, :status)
            """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed",
            },
        )
        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        self.cur.execute(
            """
                SELECT * FROM shipment
                WHERE id = ?
            """,
            (id,),
        )
        row = self.cur.fetchone()

        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        self.cur.execute(
            """
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()

        return self.get(id)

    def delete(self, id: int):
        self.cur.execute(
            """
            DELETE FROM shipment
            WHERE id = ?
        """,
            (id,),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
