"""re-initialized db after dropping all tables

Revision ID: 7d716967a0c2
Revises: None
Create Date: 2018-03-10 14:08:08.896377

"""

# revision identifiers, used by Alembic.
revision = '7d716967a0c2'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insured',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('test', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('air_id', sa.String(length=20), nullable=True),
    sa.Column('mailing_street', sa.String(length=64), nullable=True),
    sa.Column('mailing_optional', sa.String(length=64), nullable=True),
    sa.Column('mailing_city', sa.String(length=64), nullable=True),
    sa.Column('mailing_state', sa.String(length=15), nullable=True),
    sa.Column('mailing_zip', sa.String(length=10), nullable=True),
    sa.Column('mailing_country', sa.String(length=30), nullable=True),
    sa.Column('residence_country', sa.String(length=30), nullable=True),
    sa.Column('foreign_currency_default', sa.String(length=30), nullable=True),
    sa.Column('other_coverage', sa.String(length=1), nullable=True),
    sa.Column('other_insurance_co', sa.String(length=64), nullable=True),
    sa.Column('other_plan_name', sa.String(length=64), nullable=True),
    sa.Column('other_plan_id', sa.String(length=64), nullable=True),
    sa.Column('medicare_part_a', sa.String(length=1), nullable=True),
    sa.Column('medicare_part_b', sa.String(length=1), nullable=True),
    sa.Column('medicare_id', sa.String(length=64), nullable=True),
    sa.Column('full_time_student', sa.String(length=1), nullable=True),
    sa.Column('has_dependent', sa.Boolean(), nullable=True),
    sa.Column('string_test', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_insured_email'), 'insured', ['email'], unique=True)
    op.create_index(op.f('ix_insured_username'), 'insured', ['username'], unique=True)
    op.create_table('dependent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insured_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('middle_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('test', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['insured_id'], ['insured.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('claim',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insured_id', sa.Integer(), nullable=False),
    sa.Column('dependent_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dependent_id'], ['dependent.id'], ),
    sa.ForeignKeyConstraint(['insured_id'], ['insured.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_claim_timestamp'), 'claim', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_claim_timestamp'), table_name='claim')
    op.drop_table('claim')
    op.drop_table('dependent')
    op.drop_index(op.f('ix_insured_username'), table_name='insured')
    op.drop_index(op.f('ix_insured_email'), table_name='insured')
    op.drop_table('insured')
    # ### end Alembic commands ###
