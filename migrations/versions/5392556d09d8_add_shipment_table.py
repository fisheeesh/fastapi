"""add shipment table

Revision ID: 5392556d09d8
Revises:
Create Date: 2025-10-10 16:48:16.953247

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5392556d09d8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ? I can go aheas and write the code to create a db table with my preferred columns
def upgrade() -> None:
    op.create_table(
        "shipment",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("content", sa.CHAR, nullable=False),
        sa.Column("status", sa.CHAR, nullable=False),
    )


# ? I can go ahead and write code to delete that table
def downgrade() -> None:
    op.drop_table("shipment")
