"""Add device column to User model

Revision ID: 136e2f30966e
Revises: 545a7bb758eb
Create Date: 2025-05-03 18:38:33.545692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '136e2f30966e'
down_revision: Union[str, None] = '545a7bb758eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
