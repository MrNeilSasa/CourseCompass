"""empty message

Revision ID: 5995e20cd9e9
Revises: 5cff8c05783b
Create Date: 2023-06-10 20:58:47.665912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5995e20cd9e9'
down_revision = '5cff8c05783b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('prerequisites',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('prerequisites',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###
