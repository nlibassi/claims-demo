"""minor changes to virtual fields (claims) in insured and dependent tables

Revision ID: 65a4de138a10
Revises: None
Create Date: 2018-03-01 07:21:50.733212

"""

# revision identifiers, used by Alembic.
revision = '65a4de138a10'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dependent', 'insured_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dependent', 'insured_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
