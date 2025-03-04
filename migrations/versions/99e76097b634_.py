"""empty message

Revision ID: 99e76097b634
Revises: 7aca8519ac78
Create Date: 2021-11-05 15:20:49.814578

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '99e76097b634'
down_revision = '7aca8519ac78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('registered_at', sa.DateTime(), nullable=True))
    op.drop_column('customer', 'register_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('register_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('customer', 'registered_at')
    # ### end Alembic commands ###
