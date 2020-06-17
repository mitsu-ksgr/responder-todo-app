"""add location column to users table

Revision ID: aa06de249ce6
Revises: 0396244e8456
Create Date: 2020-06-14 04:49:45.746112+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa06de249ce6'
down_revision = '0396244e8456'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('location', sa.String(255)))

def downgrade():
    op.drop_column('users', 'location')

