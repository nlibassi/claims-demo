"""made ininsured_id and dependent_id fields of claim table not nullable

Revision ID: 133ac6312bf2
Revises: 65a4de138a10
Create Date: 2018-03-08 06:52:27.662759

"""

# revision identifiers, used by Alembic.
revision = '133ac6312bf2'
down_revision = '65a4de138a10'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('claim', 'dependent_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('claim', 'insured_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('claim', 'insured_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('claim', 'dependent_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
