"""Add Ticket_no to Bookin

Revision ID: a6286b45c752
Revises: c9f36648f6f0
Create Date: 2024-07-10 10:53:34.858380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6286b45c752'
down_revision = 'c9f36648f6f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_user',
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_user')
    op.drop_table('role')
    # ### end Alembic commands ###
