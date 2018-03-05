"""added fifirst, middle, last names to insured as test

Revision ID: 135123d33ac7
Revises: fdcd108f5bc0
Create Date: 2018-02-17 08:06:10.817518

"""

# revision identifiers, used by Alembic.
revision = '135123d33ac7'
down_revision = 'fdcd108f5bc0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insured', sa.Column('first_name', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('last_name', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('middle_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insured', 'middle_name')
    op.drop_column('insured', 'last_name')
    op.drop_column('insured', 'first_name')
    # ### end Alembic commands ###