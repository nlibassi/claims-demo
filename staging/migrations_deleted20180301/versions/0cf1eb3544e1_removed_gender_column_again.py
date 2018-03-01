"""removed gender column again

Revision ID: 0cf1eb3544e1
Revises: 1a796f2480f9
Create Date: 2018-02-25 21:02:32.826321

"""

# revision identifiers, used by Alembic.
revision = '0cf1eb3544e1'
down_revision = '1a796f2480f9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insured', 'gender')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insured', sa.Column('gender', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
