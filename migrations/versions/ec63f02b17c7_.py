"""empty message

Revision ID: ec63f02b17c7
Revises: 
Create Date: 2019-08-27 15:47:55.319267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec63f02b17c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('role', sa.String(length=255), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_owners_email'), 'owners', ['email'], unique=True)
    op.create_index(op.f('ix_owners_name'), 'owners', ['name'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_plate', sa.String(length=10), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_number_plate'), 'assets', ['number_plate'], unique=False)
    op.create_table('staffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('staff_no', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('staff_no')
    )
    op.create_index(op.f('ix_staffs_email'), 'staffs', ['email'], unique=True)
    op.create_index(op.f('ix_staffs_name'), 'staffs', ['name'], unique=False)
    op.create_table('trips',
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
    op.create_index(op.f('ix_trips_route'), 'trips', ['route'], unique=False)
    op.create_index(op.f('ix_trips_station'), 'trips', ['station'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trips_station'), table_name='trips')
    op.drop_index(op.f('ix_trips_route'), table_name='trips')
    op.drop_table('trips')
    op.drop_index(op.f('ix_staffs_name'), table_name='staffs')
    op.drop_index(op.f('ix_staffs_email'), table_name='staffs')
    op.drop_table('staffs')
    op.drop_index(op.f('ix_assets_number_plate'), table_name='assets')
    op.drop_table('assets')
    op.drop_table('roles')
    op.drop_index(op.f('ix_owners_name'), table_name='owners')
    op.drop_index(op.f('ix_owners_email'), table_name='owners')
    op.drop_table('owners')
    # ### end Alembic commands ###
