"""add unique constraint to users.email

Revision ID: 8e7078780851
Revises: 
Create Date: 2025-12-16 10:26:15.500394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e7078780851'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"]
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique"
    )
    pass
