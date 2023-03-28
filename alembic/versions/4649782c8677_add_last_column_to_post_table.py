"""add last column to post table

Revision ID: 4649782c8677
Revises: c7369e05b462
Create Date: 2023-03-27 16:09:44.125225

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4649782c8677'
down_revision = 'c7369e05b462'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('published', sa.Boolean(),
                                    nullable=False, server_default='TRUE'),)
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(),
                                    nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
