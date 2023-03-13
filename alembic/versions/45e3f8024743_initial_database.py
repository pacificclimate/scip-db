"""initial database

Revision ID: 45e3f8024743
Revises: 
Create Date: 2023-03-10 16:06:22.095412

"""
### brings a blank database up to the initial version of the salmon database design

from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa


revision = '45e3f8024743'
down_revision = None
branch_labels = None
depends_on = None

salmon_schema='salmon_geometry' #change if needed


def upgrade() -> None:
    op.create_table('conservation_unit',
    sa.Column('conservation_unit_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('boundary', Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('outlet', Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('conservation_unit_id'),
    schema=salmon_schema
    )
    op.create_table('reference',
    sa.Column('reference_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('abbrev_cite', sa.String(), nullable=True),
    sa.Column('full_citation', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('reference_id'),
    schema=salmon_schema
    )
    op.create_table('region',
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('kind', sa.Enum('basin', 'watershed', name='region_kinds'), nullable=True),
    sa.Column('boundary', Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('outlet', Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('region_id'),
    schema=salmon_schema
    )
    op.create_table('taxon',
    sa.Column('taxon_id', sa.Integer(), nullable=False),
    sa.Column('common_name', sa.String(), nullable=True),
    sa.Column('scientific_name', sa.String(), nullable=True),
    sa.Column('subgroup', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('taxon_id'),
    schema=salmon_schema
    )
    op.create_table('phenology',
    sa.Column('phenology_id', sa.Integer(), nullable=False),
    sa.Column('minimum', sa.Float(), nullable=True),
    sa.Column('maximum', sa.Float(), nullable=True),
    sa.Column('mean', sa.Float(), nullable=True),
    sa.Column('standard_deviation', sa.Float(), nullable=True),
    sa.Column('data_reference', sa.Integer(), nullable=True),
    sa.Column('precise_time_reference', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['data_reference'], [f"{salmon_schema}.reference.reference_id"], ),
    sa.ForeignKeyConstraint(['precise_time_reference'], [f"{salmon_schema}.reference.reference_id"], ),
    sa.PrimaryKeyConstraint('phenology_id'),
    schema=salmon_schema
    )
    op.create_table('population',
    sa.Column('population_id', sa.Integer(), nullable=False),
    sa.Column('taxon_id', sa.Integer(), nullable=True),
    sa.Column('conservation_unit_id', sa.Integer(), nullable=True),
    sa.Column('overwinter', sa.Boolean(), nullable=True),
    sa.Column('extinct', sa.Boolean(), nullable=True),
    sa.Column('spawn_time_range', sa.Integer(), nullable=True),
    sa.Column('migration_time_range', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['conservation_unit_id'], [f"{salmon_schema}.conservation_unit.conservation_unit_id"], ),
    sa.ForeignKeyConstraint(['migration_time_range'], [f"{salmon_schema}.phenology.phenology_id"], ),
    sa.ForeignKeyConstraint(['spawn_time_range'], [f"{salmon_schema}.phenology.phenology_id"], ),
    sa.ForeignKeyConstraint(['taxon_id'], [f"{salmon_schema}.taxon.taxon_id"], ),
    sa.PrimaryKeyConstraint('population_id'),
    schema=salmon_schema
    )

def downgrade() -> None:
    op.drop_table('population', schema='salmon_geometry')
    op.drop_table('phenology', schema='salmon_geometry')
    op.drop_table('taxon', schema='salmon_geometry')
    op.drop_table('region', schema='salmon_geometry')
    op.drop_table('reference', schema='salmon_geometry')
    op.drop_table('conservation_unit', schema='salmon_geometry')
    op.drop_enum('region_kinds', schema='salmon_geometry')
    # ### end Alembic commands ###
