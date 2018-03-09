"""maalloweddependent_id column of claim table to be nullable

Revision ID: 38f583af10c8
Revises: 133ac6312bf2
Create Date: 2018-03-08 07:03:40.077855

"""

# revision identifiers, used by Alembic.
revision = '38f583af10c8'
down_revision = '133ac6312bf2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('claim', 'dependent_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('claim', 'dependent_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
