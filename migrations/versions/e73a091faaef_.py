"""empty message

Revision ID: e73a091faaef
Revises: cb53ebdedf77
Create Date: 2021-11-05 15:45:00.601673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e73a091faaef'
down_revision = 'cb53ebdedf77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone', sa.String(), nullable=True))
    op.drop_column('customer', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('customer', 'phone')
    # ### end Alembic commands ###
