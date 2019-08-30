"""migrations

Revision ID: b1e2e84ca21a
Revises: b714a7e1164b
Create Date: 2019-08-29 00:07:01.472392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e2e84ca21a'
down_revision = 'b714a7e1164b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('routes', sa.Column('trip_total_fare', sa.String(length=70), nullable=True))
    op.create_index(op.f('ix_routes_trip_total_fare'), 'routes', ['trip_total_fare'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_routes_trip_total_fare'), table_name='routes')
    op.drop_column('routes', 'trip_total_fare')
    # ### end Alembic commands ###