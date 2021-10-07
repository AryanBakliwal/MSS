# flake8: noqa
"""
DB setup until v6.x

Revision ID: cd8b7108713a
Revises: 
Create Date: 2021-10-04 09:10:35.606793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd8b7108713a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('emailid', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('emailid'),
    sa.UniqueConstraint('password')
    )
    op.create_table('changes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('p_id', sa.Integer(), nullable=True),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.Column('commit_hash', sa.String(length=255), nullable=True),
    sa.Column('version_name', sa.String(length=255), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['p_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('p_id', sa.Integer(), nullable=True),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('message_type', sa.Enum('TEXT', 'SYSTEM_MESSAGE', 'IMAGE', 'DOCUMENT', name='messagetype'), nullable=True),
    sa.Column('reply_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['p_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['reply_id'], ['messages.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('p_id', sa.Integer(), nullable=True),
    sa.Column('u_id', sa.Integer(), nullable=True),
    sa.Column('access_level', sa.Enum('admin', 'collaborator', 'viewer', 'creator', name='access_level'), nullable=True),
    sa.ForeignKeyConstraint(['p_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permissions')
    op.drop_table('messages')
    op.drop_table('changes')
    op.drop_table('users')
    op.drop_table('projects')
    # ### end Alembic commands ###