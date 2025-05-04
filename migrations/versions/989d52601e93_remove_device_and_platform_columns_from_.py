"""Remove device and platform columns from User model

Revision ID: 989d52601e93
Revises: 136e2f30966e
Create Date: 2025-05-03 18:45:33.945454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '989d52601e93'
down_revision: Union[str, None] = '136e2f30966e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
