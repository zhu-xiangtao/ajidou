"""empty message

Revision ID: 2e3fd1e4384b
Revises: ea07af79c409
Create Date: 2019-10-14 21:34:05.351000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e3fd1e4384b'
down_revision = 'ea07af79c409'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_runner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('creater', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=True),
    sa.Column('status', sa.String(length=8), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('runner_case',
    sa.Column('runner_id', sa.Integer(), nullable=False),
    sa.Column('csae_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['csae_id'], ['test_case.id'], ),
    sa.ForeignKeyConstraint(['runner_id'], ['test_runner.id'], ),
    sa.PrimaryKeyConstraint('runner_id', 'csae_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('runner_case')
    op.drop_table('test_runner')
    # ### end Alembic commands ###
