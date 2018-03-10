"""adadded 16 columns to Insured

Revision ID: 431d5cd12fd7
Revises: 292ab5979b98
Create Date: 2018-03-10 12:17:48.845950

"""

# revision identifiers, used by Alembic.
revision = '431d5cd12fd7'
down_revision = '292ab5979b98'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insured', sa.Column('foreign_currency_default', sa.String(length=30), nullable=True))
    op.add_column('insured', sa.Column('full_time_student', sa.Boolean(), nullable=True))
    op.add_column('insured', sa.Column('mailing_city', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('mailing_country', sa.String(length=30), nullable=True))
    op.add_column('insured', sa.Column('mailing_optional', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('mailing_state', sa.String(length=15), nullable=True))
    op.add_column('insured', sa.Column('mailing_street', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('mailing_zip', sa.String(length=10), nullable=True))
    op.add_column('insured', sa.Column('medicare_id', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('medicare_part_a', sa.Boolean(), nullable=True))
    op.add_column('insured', sa.Column('medicare_part_b', sa.Boolean(), nullable=True))
    op.add_column('insured', sa.Column('other_coverage', sa.Boolean(), nullable=True))
    op.add_column('insured', sa.Column('other_insurance_co', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('other_plan_id', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('other_plan_name', sa.String(length=64), nullable=True))
    op.add_column('insured', sa.Column('residence_country', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insured', 'residence_country')
    op.drop_column('insured', 'other_plan_name')
    op.drop_column('insured', 'other_plan_id')
    op.drop_column('insured', 'other_insurance_co')
    op.drop_column('insured', 'other_coverage')
    op.drop_column('insured', 'medicare_part_b')
    op.drop_column('insured', 'medicare_part_a')
    op.drop_column('insured', 'medicare_id')
    op.drop_column('insured', 'mailing_zip')
    op.drop_column('insured', 'mailing_street')
    op.drop_column('insured', 'mailing_state')
    op.drop_column('insured', 'mailing_optional')
    op.drop_column('insured', 'mailing_country')
    op.drop_column('insured', 'mailing_city')
    op.drop_column('insured', 'full_time_student')
    op.drop_column('insured', 'foreign_currency_default')
    # ### end Alembic commands ###
