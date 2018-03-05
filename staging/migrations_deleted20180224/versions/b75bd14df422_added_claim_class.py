"""added Claim class

Revision ID: b75bd14df422
Revises: 566cb089a510
Create Date: 2018-02-09 07:33:05.139840

"""

# revision identifiers, used by Alembic.
revision = 'b75bd14df422'
down_revision = '566cb089a510'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('claims',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['insureds.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_claims_timestamp'), 'claims', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_claims_timestamp'), table_name='claims')
    op.drop_table('claims')
    # ### end Alembic commands ###