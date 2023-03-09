from sqlalchemy import Column, Integer, String, Enum, Boolean, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class Region(Base):
    __tablename__="region"
    id = Column('region_id', Integer, primary_key=True)
    name=Column(String)
    code=Column(String)
    kind=Column(Enum("basin", "watershed"))
    boundary=Column(Geometry('POLYGON'))
    outlet=Column(Geometry('POINT'))
    
    
class Taxon(Base):
    __tablename__="taxon"
    id=Column('taxon_id', Integer, primary_key=True)
    common_name=Column(String)
    scientific_name=Column(String)
    subgroup=Column(String)
    
    
class ConservationUnit(Base):
    __tablename__="conservation_unit"
    id=Column('conservation_unit_id', Integer, primary_key=True)
    name=Column(String)
    code=Column(String)
    boundary=Column(Geometry('POLYGON'))
    outlet=Column(Geometry('POINT'))
    
class Reference(Base):
    __tablename__="reference"
    id=Column('reference_id', Integer, primary_key=True)
    code=Column(String)
    abbrev_cite=Column(String)
    full_citation=Column(String)
    
class Phenology(Base):
    __tablename__="phenology"
    id=Column('phenology_id', Integer, primary_key=True)
    minimum=Column(Float)
    maximum=Column(Float)
    mean=Column(Float)
    standard_deviation=Column(Float)
    data_reference=Column(
        Integer, 
        ForeignKey("reference.reference_id"))
    precise_time_reference=Column(
        Integer, 
        ForeignKey("reference.reference_id"))
        
    
class Population(Base):
    __tablename__="population"
    id=Column('population_id', Integer, primary_key=True)
    taxon_id=Column(
        Integer,
        ForeignKey('taxon.taxon_id'))
    conservation_unit_id=Column(
        Integer,
        ForeignKey('conservation_unit.conservation_unit_id'))
    overwinter=Column(Boolean)
    extinct=Column(Boolean)
    spawn_time_range=Column(
        Integer,
        ForeignKey("phenology.phenology_id"))
    migration_time_range=Column(
        Integer,
        ForeignKey("phenology.phenology_id"))