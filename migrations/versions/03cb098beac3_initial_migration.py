"""Initial migration

Revision ID: 03cb098beac3
Revises: 
Create Date: 2024-09-13 11:57:24.242817

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03cb098beac3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carbon_footprint',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('call_id', sa.Integer(), nullable=False),
    sa.Column('energy_consumption', sa.Float(), nullable=False),
    sa.Column('carbon_emissions', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['call_id'], ['video_call.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recommendation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recommendation_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('video_call', schema=None) as batch_op:
        batch_op.alter_column('device_specs',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=sa.JSON(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('video_call', schema=None) as batch_op:
        batch_op.alter_column('device_specs',
               existing_type=sa.JSON(),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=False)

    op.drop_table('recommendation')
    op.drop_table('carbon_footprint')
    # ### end Alembic commands ###
