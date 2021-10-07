# flake8: noqa
"""

DB setup 6.x

Revision ID: 83993fcdf5ef
Revises: cd8b7108713a
Create Date: 2021-10-04 09:22:36.987652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83993fcdf5ef'
down_revision = 'cd8b7108713a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.drop_table('projects')
    with op.batch_alter_table('changes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('op_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'operations', ['op_id'], ['id'])
        batch_op.drop_column('p_id')

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('op_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'operations', ['op_id'], ['id'])
        batch_op.drop_column('p_id')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('op_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'operations', ['op_id'], ['id'])
        batch_op.drop_column('p_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registered_on', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('confirmed_on', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('confirmed_on')
        batch_op.drop_column('confirmed')
        batch_op.drop_column('registered_on')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('p_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'projects', ['p_id'], ['id'])
        batch_op.drop_column('op_id')

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('p_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'projects', ['p_id'], ['id'])
        batch_op.drop_column('op_id')

    with op.batch_alter_table('changes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('p_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'projects', ['p_id'], ['id'])
        batch_op.drop_column('op_id')

    op.create_table('projects',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('path', sa.VARCHAR(length=255), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.drop_table('operations')
    # ### end Alembic commands ###