"""adds Routes model

Revision ID: a812f84d658a
Revises: 107b896fe8fe
Create Date: 2019-08-22 13:07:52.866037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a812f84d658a'
down_revision = '107b896fe8fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_plate', sa.Integer(), nullable=True),
    sa.Column('route', sa.String(length=255), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('fare', sa.String(length=10), nullable=True),
    sa.Column('station', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['number_plate'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fare'),
    sa.UniqueConstraint('passengers')
    )
    op.create_index(op.f('ix_routes_route'), 'routes', ['route'], unique=False)
    op.create_index(op.f('ix_routes_station'), 'routes', ['station'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_routes_station'), table_name='routes')
    op.drop_index(op.f('ix_routes_route'), table_name='routes')
    op.drop_table('routes')
    # ### end Alembic commands ###