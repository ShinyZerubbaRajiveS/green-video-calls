"""Fix duration column type to Float

Revision ID: 98cfb9e6b22b
Revises: 50940a6252a1
Create Date: 2025-05-03 23:21:33.656122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98cfb9e6b22b'
down_revision: Union[str, None] = '50940a6252a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
