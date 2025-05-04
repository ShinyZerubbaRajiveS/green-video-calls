"""Added foreign key relationship between video_call and carbon_footprint

Revision ID: 28e678ec60f3
Revises: 989d52601e93
Create Date: 2025-05-03 18:53:58.665516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28e678ec60f3'
down_revision: Union[str, None] = '989d52601e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
