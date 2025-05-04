"""Initial tables

Revision ID: 65fa25529dcd
Revises: 33d7ec1e173b
Create Date: 2025-05-04 12:33:23.886240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65fa25529dcd'
down_revision: Union[str, None] = '33d7ec1e173b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
