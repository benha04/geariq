"""create tracks table

Revision ID: 0001_create_tracks_table
Revises: 
Create Date: 2025-11-12
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_tracks_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tracks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('q', sa.String(length=512), nullable=False),
        sa.Column('budget', sa.Float, nullable=True),
        sa.Column('contact', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('tracks')
