# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      02a_Point_Creation.py
# Description:  Creates points in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")


### Creating Points

# The options and settings for creating all geometry in LUSAS is defined in the IFGeometryData object.
# To start any geometry creation, get the geometryData object and set all the defaults
geometry_data = lusas.geometryData().setAllDefaults()
# Here we are creating points by specifying the coordinates, we set the option in setLowerOrderGeometryType
geometry_data.setLowerOrderGeometryType("coordinates")

# Now we add the point coordinates
geometry_data.addCoords(1.0, 1.0, 0.0)
geometry_data.addCoords(2.0, 2.0, 0.0)

# Now we instruct the database to the create the points. It will return an IFObject set containing the newly created points
object_set:'IFObjectSet' = lusas.database().createPoint(geometry_data)

# Get all points from the returned object set
points:list['IFPoint'] = object_set.getObjects("Point")

# Loop through the points and print their IDs and coordinates
for point in points:
    print(f"Point: {point.getID()} at coordinates ({point.getX()},{point.getY()},{point.getZ()})")


### Using Helper function
# The Helper module contains some useful functions to simplify the geometry creation process.

# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)

# Points creation:
point1 = Helpers.create_point(2.0, 1.0, 0.0)
point2 = Helpers.create_point(3.0, 2.0, 0.0)
