"""create users table

Revision ID: 2b1868168ec4
Revises:
Create Date: 2024-06-21 22:01:19.123674

"""
from alembic import op
import sqlalchemy as sa

revision = '2b1868168ec4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email_verified_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('avatar', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=15), nullable=False, default='active'),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('remember_token', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade():
    op.drop_table('users')
