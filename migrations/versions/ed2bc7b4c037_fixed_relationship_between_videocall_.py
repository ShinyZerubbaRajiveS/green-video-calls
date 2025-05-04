"""Fixed relationship between VideoCall and CarbonFootprint

Revision ID: ed2bc7b4c037
Revises: 28e678ec60f3
Create Date: 2025-05-03 18:59:06.909785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed2bc7b4c037'
down_revision: Union[str, None] = '28e678ec60f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
