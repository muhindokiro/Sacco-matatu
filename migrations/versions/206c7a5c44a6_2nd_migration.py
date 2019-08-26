"""2nd Migration

Revision ID: 206c7a5c44a6
Revises: 661e7340ff07
Create Date: 2019-08-26 13:00:22.427296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '206c7a5c44a6'
down_revision = '661e7340ff07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('conductor', sa.String(length=70), nullable=True))
    op.add_column('routes', sa.Column('driver', sa.String(length=70), nullable=True))
    op.create_index(op.f('ix_routes_conductor'), 'routes', ['conductor'], unique=False)
    op.create_index(op.f('ix_routes_driver'), 'routes', ['driver'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_routes_driver'), table_name='routes')
    op.drop_index(op.f('ix_routes_conductor'), table_name='routes')
    op.drop_column('routes', 'driver')
    op.drop_column('routes', 'conductor')
    # ### end Alembic commands ###
