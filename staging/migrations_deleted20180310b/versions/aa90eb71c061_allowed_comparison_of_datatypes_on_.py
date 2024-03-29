"""allowed comparison of datatypes on columns

Revision ID: aa90eb71c061
Revises: None
Create Date: 2018-03-10 14:01:27.223142

"""

# revision identifiers, used by Alembic.
revision = 'aa90eb71c061'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('insured', 'full_time_student',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=1),
               existing_nullable=True)
    op.alter_column('insured', 'gender',
               existing_type=sa.VARCHAR(length=15),
               type_=sa.String(length=1),
               existing_nullable=True)
    op.alter_column('insured', 'medicare_part_a',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=1),
               existing_nullable=True)
    op.alter_column('insured', 'medicare_part_b',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=1),
               existing_nullable=True)
    op.alter_column('insured', 'other_coverage',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=1),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('insured', 'other_coverage',
               existing_type=sa.String(length=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('insured', 'medicare_part_b',
               existing_type=sa.String(length=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('insured', 'medicare_part_a',
               existing_type=sa.String(length=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('insured', 'gender',
               existing_type=sa.String(length=1),
               type_=sa.VARCHAR(length=15),
               existing_nullable=True)
    op.alter_column('insured', 'full_time_student',
               existing_type=sa.String(length=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    # ### end Alembic commands ###
