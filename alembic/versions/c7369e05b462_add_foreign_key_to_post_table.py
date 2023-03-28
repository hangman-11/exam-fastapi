"""add foreign key to post table

Revision ID: c7369e05b462
Revises: e06f4a33e3c7
Create Date: 2023-03-25 15:51:57.856171

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c7369e05b462'
down_revision = 'e06f4a33e3c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='post', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='post')
    op.drop_column('post', 'owner_id')
    pass
