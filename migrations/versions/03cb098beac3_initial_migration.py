from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '03cb098beac3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop the password column if it exists
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')

    # Ensure the video_call table is properly set up with the correct foreign key constraint
    with op.batch_alter_table('video_call', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_user', 
            'users', 
            ['user_id'], 
            ['id']
        )

def downgrade():
    # Reverse the operations in downgrade if needed
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=255)))

    with op.batch_alter_table('video_call', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user', type_='foreignkey')
