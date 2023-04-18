# This script accepts a shapefile and adds all polygon features found in the file to the 
# associated database. A feature must have a "name" and a "code". A feature may optionally
# have an outlet, consisting of a latitude component and a longitude component. 
# The correspondence between database attribute names and shapefile attribute names is
# provided via a .yaml file.
#
# The kind of region (watershed, basin, conservation_unit) is supplied as an argument
# to this script.
#
# Note that if a region is already in the database, defined as having the same code 
# and the same kind as a region already in the database, this script will update the
# name, boundary, and outlet of the feature to to match the new data.

import argparse
import yaml
from osgeo import ogr
import logging
import traceback
from salmon_occurrence import Region
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
 
parser = argparse.ArgumentParser('Add data from a shapefile to the salmon daatabase')
parser.add_argument('shapefile', help='a shapefile with regions to be added')
parser.add_argument('yaml', help='a yaml file with correspondances between attributes')
parser.add_argument('kind', help='the type of region this is', choices=['basin', 'watershed', 'conservation_unit'])
parser.add_argument('dsn', help='database connection string')
parser.add_argument('-d', '--dry', help='dry run to check data format and database connection', action='store_true')
 
args = parser.parse_args()


needed_fields = ['name', 'code']
outlet_fields = ['outlet_lat', 'outlet_lon']

#set up logging
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



if args.dry:
    logger.info("Dry Run")
else: 
    logger.info("Adding Regions")

try:
    att_dict = {}
    outlet_missing = False

    #load yaml
    with open(args.yaml, 'r') as yaml_file:
        logger.info("Loading yaml")
        correspondance = yaml.safe_load(yaml_file)
        for att in needed_fields:
            if correspondance[att]:
                att_dict[att] = correspondance[att]
                logger.info("Inputting {} from {}".format(att, correspondance[att]))
            else:
                raise Exception("Missing {} attribute in {}".format(att, args.yaml))
        for att in outlet_fields:
            if correspondance[att]:
                att_dict[att] = correspondance[att]
                logger.info("Inputting {} from {}".format(att, correspondance[att]))
            else:
                outlet_missing = True

        if outlet_missing:
            logger.warn("Outlet data not available")
            for att in outlet_fields:
                if att in correspondance:
                    correspondance.pop(att)
        else:
            logger.info("Outlet attributes found, will load outlet data")

    # load shapefile
    logger.info("Loading shapefile")
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shapefile = driver.Open(args.shapefile)
    
    if shapefile is None:
        raise Exception("Could not open shapefile {}".format(args.shapefile))
            
    #see if the attribute we are looking for are present
    logger.info("Checking shapefile attributes")
    layer = shapefile.GetLayer(0) #shapefiles have only one layer
    layer_definition = layer.GetLayerDefn()
        
    fields = []
    #get a list of all fields.
    for i in range(layer_definition.GetFieldCount()):
        fields.append(layer_definition.GetFieldDefn(i).GetName())
    
    for att in correspondance:
        if correspondance[att] in fields:
            logger.info("{} present in shapefile".format(correspondance[att]))
        else:
            raise Exception("Attribute {} not present in shapefile".format(correspondance[att]))
    
    logger.info("All expected attributes present in shapefile")
    
    # connect to database
    engine = create_engine(args.dsn)
    Session = sessionmaker(bind=engine)
    
    # try to add areas
    # TODO: if area already present, update instead of add!
    def getFeatureAttributeByName(layer, feature, attribute):
        # as far as I can tell, features are only addressable by numerical index.
        # this returns the value of an attribute, given its name
        for i in range(0, layer.GetLayerDefn().GetFieldCount()):
            field_name = layer.GetLayerDefn().GetFieldDefn(i).GetName()
            if field_name == attribute:
                return feature.GetField(i)
        # attribute not found - shouldn't happen under normal circumstances
        raise Exception("Attribute {} not present in a feature".format(attribute))
        
    
    region_count = 0
    multipolygon_count = 0
    session = Session()
    session.execute(text('SET search_path TO salmon_geometry'))

    for feature in layer:
        fname = getFeatureAttributeByName(layer, feature, correspondance["name"])
        fcode = getFeatureAttributeByName(layer, feature, correspondance["code"])
        
        foutlet = 'POINT EMPTY'
        if not outlet_missing:
            flat = getFeatureAttributeByName(layer, feature, correspondance["outlet_lat"])
            flon = getFeatureAttributeByName(layer, feature, correspondance["outlet_lon"])
            if flat and flon:
                foutlet = 'POINT({} {})'.format(flon, flat)

                
        fboundary = feature.GetGeometryRef().ExportToWkt()
        
        #if region consists of multiple polygons (island regions), skip it for now.
        #TODO: make multipolygons into some sort of merged shape.
        if fboundary.startswith("POLYGON"):
            region = Region(
                kind=args.kind,
                name=fname,
                code=fcode,
                boundary=text("'{}'".format(fboundary)),
                outlet=text("'{}'".format(foutlet))
            )

            logger.info("Adding region {} {} outlet data".format(fname, "without" if foutlet == 'POINT EMPTY' else "with"))
            
            if not args.dry:
                session.add(region)
                session.commit()
            region_count = region_count + 1
        else:
            logger.warning("Could not add region {} as it is not a single polygon".format(fname))
            multipolygon_count = multipolygon_count + 1

    if args.dry:
        final_message = "DRY RUN: {} potential {}s to add found, {} {}s cannot be added because they were multipolygons"
    else:
        final_message = "{} {}s added, {} {}s were multipolygons and could not be added"
    logger.info(final_message.format(region_count, args.kind, multipolygon_count, args.kind))
    session.close()
        
        



except Exception as e:
    logger.error(traceback.format_exc())
    
finally:
    print("Finished")