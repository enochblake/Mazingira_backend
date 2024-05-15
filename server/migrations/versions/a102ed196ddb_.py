"""empty message

Revision ID: a102ed196ddb
Revises: abbaa6c59688
Create Date: 2024-05-15 11:03:42.964326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a102ed196ddb'
down_revision = 'abbaa6c59688'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
