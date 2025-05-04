"""empty message

Revision ID: 2b9a828b206c
Revises: ed2bc7b4c037
Create Date: 2025-05-03 20:56:59.321160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b9a828b206c'
down_revision: Union[str, None] = 'ed2bc7b4c037'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
