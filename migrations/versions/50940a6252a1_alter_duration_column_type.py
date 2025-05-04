"""Alter duration column type

Revision ID: 50940a6252a1
Revises: 3cda7df9797a
Create Date: 2025-05-03 23:10:36.608739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50940a6252a1'
down_revision: Union[str, None] = '3cda7df9797a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
