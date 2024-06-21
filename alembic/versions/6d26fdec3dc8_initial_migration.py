"""initial migration

Revision ID: 6d26fdec3dc8
Revises: 
Create Date: 2024-06-20 06:05:33.651920

"""

from alembic import op
import sqlalchemy as sa

# Declare the revision variable explicitly
revision = '6d26fdec3dc8'
down_revision = None

def upgrade():
    # Example of table creation
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), unique=True, nullable=True),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    pass

def downgrade():
    op.drop_table('users')
    pass
