"""moved nanames from Insured to Profile, added test columns to Profile

Revision ID: 72865ec2589c
Revises: 135123d33ac7
Create Date: 2018-02-22 07:21:26.534567

"""

# revision identifiers, used by Alembic.
revision = '72865ec2589c'
down_revision = '135123d33ac7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insured_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('relationship_to_employee', sa.Integer(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['insured_id'], ['insured.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('insured', 'first_name')
    op.drop_column('insured', 'last_name')
    op.drop_column('insured', 'middle_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insured', sa.Column('middle_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('insured', sa.Column('last_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('insured', sa.Column('first_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_table('profile')
    # ### end Alembic commands ###
