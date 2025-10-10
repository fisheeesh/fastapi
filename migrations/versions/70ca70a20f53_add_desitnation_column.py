"""add desitnation column

Revision ID: 70ca70a20f53
Revises: 5392556d09d8
Create Date: 2025-10-10 16:56:37.005241

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70ca70a20f53"
down_revision: Union[str, None] = "5392556d09d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "shipment",
        sa.Column(
            "destination",
            sa.INTEGER,
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "shipment",
        "destination",
    )
