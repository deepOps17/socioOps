"""add content column to posts table

Revision ID: 73f3f58b5517
Revises: 7eb5010626b6
Create Date: 2022-09-21 10:22:09.103901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73f3f58b5517'
down_revision = '7eb5010626b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
