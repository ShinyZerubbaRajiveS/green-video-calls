"""Set explicit table names and fix foreign keys

Revision ID: 3cda7df9797a
Revises: 2b9a828b206c
Create Date: 2025-05-03 22:59:37.506509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cda7df9797a'
down_revision: Union[str, None] = '2b9a828b206c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
