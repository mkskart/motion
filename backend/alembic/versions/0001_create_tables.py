"""create tables

Revision ID: 0001
Revises: 
Create Date: 2025-04-28 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String),
        sa.Column('google_sub', sa.String, unique=True),
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('duration_minutes', sa.Integer, default=60),
        sa.Column('priority', sa.Enum('high', 'medium', 'low', name='priority')),
        sa.Column('scheduled_start', sa.DateTime),
        sa.Column('scheduled_end', sa.DateTime),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
    )

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
