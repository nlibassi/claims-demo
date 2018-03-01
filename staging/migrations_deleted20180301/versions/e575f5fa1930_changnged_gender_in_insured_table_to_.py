"""changnged gender in insured table to string type for now

Revision ID: e575f5fa1930
Revises: 27ec081ae453
Create Date: 2018-02-24 11:53:50.909707

"""

# revision identifiers, used by Alembic.
revision = 'e575f5fa1930'
down_revision = '27ec081ae453'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insured', 'date_of_birth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insured', sa.Column('date_of_birth', sa.DATE(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
