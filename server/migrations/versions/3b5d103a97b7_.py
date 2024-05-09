"""empty message

Revision ID: 3b5d103a97b7
Revises: d166c78bebc7
Create Date: 2024-05-09 20:32:00.978309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b5d103a97b7'
down_revision = 'd166c78bebc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.alter_column('organization_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.alter_column('organization_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
