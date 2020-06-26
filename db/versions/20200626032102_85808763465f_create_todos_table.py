"""create todos table

Revision ID: 85808763465f
Revises: aa06de249ce6
Create Date: 2020-06-26 03:21:02.569126+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85808763465f'
down_revision = 'aa06de249ce6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('status', sa.String(255)),
        sa.Column('description', sa.Text),
        sa.Column('due_date', sa.DateTime),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('todos')

