"""Change completed_at column to String

Revision ID: f0a01c6b9961
Revises: c8ee4fbe3847
Create Date: 2023-11-27 20:15:07.843729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0a01c6b9961'
down_revision = 'c8ee4fbe3847'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('completed_at',
               existing_type=sa.DATETIME(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('completed_at',
               existing_type=sa.String(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###