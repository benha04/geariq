"""add product vector column

Revision ID: 0002_add_product_vector
Revises: 0001_create_tracks_table
Create Date: 2025-11-12
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_product_vector'
down_revision = '0001_create_tracks_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add a vector column using pgvector extension type. If pgvector isn't available,
    # this may need to be run in a DB with the extension installed.
    op.add_column('products', sa.Column('vector', sa.dialects.postgresql.ARRAY(sa.Float), nullable=True))
    # create a GIN index for vector similarity search using pgvector extension functions is
    # database-specific; create a simple btree NULL index fallback for portability
    try:
        op.create_index('ix_products_vector_gin', 'products', ['vector'], postgresql_using='gin')
    except Exception:
        op.create_index('ix_products_vector_fallback', 'products', ['vector'])


def downgrade() -> None:
    try:
        op.drop_index('ix_products_vector_gin', table_name='products')
    except Exception:
        try:
            op.drop_index('ix_products_vector_fallback', table_name='products')
        except Exception:
            pass
    op.drop_column('products', 'vector')
