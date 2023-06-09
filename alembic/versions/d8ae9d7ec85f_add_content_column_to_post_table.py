"""add content column to post table

Revision ID: d8ae9d7ec85f
Revises: 556d90fe91a3
Create Date: 2023-03-25 15:16:58.806653

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd8ae9d7ec85f'
down_revision = '556d90fe91a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass
