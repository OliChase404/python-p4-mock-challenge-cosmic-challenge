"""empty message

Revision ID: 7fbf64827422
Revises: 4da77864abd4
Create Date: 2023-05-01 09:27:52.821922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fbf64827422'
down_revision = '4da77864abd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_scientists_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_scientists_name'), type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
