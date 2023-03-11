"""initial database

Revision ID: 45e3f8024743
Revises: 
Create Date: 2023-03-10 16:06:22.095412

"""
### brings a blank database up to the initial version of the salmon database design

from alembic import op
import sqlalchemy as sa


revision = '45e3f8024743'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('conservation_unit',
    sa.Column('conservation_unit_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('boundary', geoalchemy2.types.Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('outlet', geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('conservation_unit_id')
    )
    op.create_index('idx_conservation_unit_boundary', 'conservation_unit', ['boundary'], unique=False, postgresql_using='gist')
    op.create_index('idx_conservation_unit_outlet', 'conservation_unit', ['outlet'], unique=False, postgresql_using='gist')
    op.create_table('reference',
    sa.Column('reference_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('abbrev_cite', sa.String(), nullable=True),
    sa.Column('full_citation', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('reference_id')
    )
    op.create_table('region',
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('kind', sa.Enum('basin', 'watershed'), nullable=True),
    sa.Column('boundary', geoalchemy2.types.Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('outlet', geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('region_id')
    )
    op.create_index('idx_region_boundary', 'region', ['boundary'], unique=False, postgresql_using='gist')
    op.create_index('idx_region_outlet', 'region', ['outlet'], unique=False, postgresql_using='gist')
    op.create_table('taxon',
    sa.Column('taxon_id', sa.Integer(), nullable=False),
    sa.Column('common_name', sa.String(), nullable=True),
    sa.Column('scientific_name', sa.String(), nullable=True),
    sa.Column('subgroup', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('taxon_id')
    )
    op.create_table('phenology',
    sa.Column('phenology_id', sa.Integer(), nullable=False),
    sa.Column('minimum', sa.Float(), nullable=True),
    sa.Column('maximum', sa.Float(), nullable=True),
    sa.Column('mean', sa.Float(), nullable=True),
    sa.Column('standard_deviation', sa.Float(), nullable=True),
    sa.Column('data_reference', sa.Integer(), nullable=True),
    sa.Column('precise_time_reference', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_reference'], ['reference.reference_id'], ),
    sa.ForeignKeyConstraint(['precise_time_reference'], ['reference.reference_id'], ),
    sa.PrimaryKeyConstraint('phenology_id')
    )
    op.create_table('population',
    sa.Column('population_id', sa.Integer(), nullable=False),
    sa.Column('taxon_id', sa.Integer(), nullable=True),
    sa.Column('conservation_unit_id', sa.Integer(), nullable=True),
    sa.Column('overwinter', sa.Boolean(), nullable=True),
    sa.Column('extinct', sa.Boolean(), nullable=True),
    sa.Column('spawn_time_range', sa.Integer(), nullable=True),
    sa.Column('migration_time_range', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conservation_unit_id'], ['conservation_unit.conservation_unit_id'], ),
    sa.ForeignKeyConstraint(['migration_time_range'], ['phenology.phenology_id'], ),
    sa.ForeignKeyConstraint(['spawn_time_range'], ['phenology.phenology_id'], ),
    sa.ForeignKeyConstraint(['taxon_id'], ['taxon.taxon_id'], ),
    sa.PrimaryKeyConstraint('population_id')
    )

def downgrade() -> None:
    op.drop_table('population')
    op.drop_table('phenology')
    op.drop_table('taxon')
    op.drop_index('idx_region_outlet', table_name='region', postgresql_using='gist')
    op.drop_index('idx_region_boundary', table_name='region', postgresql_using='gist')
    op.drop_table('region')
    op.drop_table('reference')
    op.drop_index('idx_conservation_unit_outlet', table_name='conservation_unit', postgresql_using='gist')
    op.drop_index('idx_conservation_unit_boundary', table_name='conservation_unit', postgresql_using='gist')
    op.drop_table('conservation_unit')
    # ### end Alembic commands ###
