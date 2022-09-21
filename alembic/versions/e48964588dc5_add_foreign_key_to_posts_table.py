"""add foreign key to posts table

Revision ID: e48964588dc5
Revises: c1cf7407e10b
Create Date: 2022-09-21 10:39:06.574739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e48964588dc5'
down_revision = 'c1cf7407e10b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
            'posts_users_fk', 
            source_table='posts', 
            referent_table='users', 
            local_cols=['owner_id'],
            remote_cols=['id'],
            ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
