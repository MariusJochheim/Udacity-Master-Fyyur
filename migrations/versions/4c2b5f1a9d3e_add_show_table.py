"""add show table

Revision ID: 4c2b5f1a9d3e
Revises: bd99bea72e8d
Create Date: 2026-02-02 14:12:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2b5f1a9d3e'
down_revision = 'bd99bea72e8d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Show',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('venue_id', sa.Integer(), sa.ForeignKey('Venue.id'), nullable=False),
        sa.Column('artist_id', sa.Integer(), sa.ForeignKey('Artist.id'), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Show')
