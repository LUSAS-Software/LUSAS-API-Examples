# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      02b_Line_Creation.py
# Description:  Creates lines in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")


######################################################
### Straight line By Coordinates

# The options and settings for creating all geometry in LUSAS is defined in the IFGeometryData object.
# To start any geometry creation, get the geometryData object and set all the defaults
geometry_data = lusas.geometryData().setAllDefaults()
# Here we are creating a line by specifying the coordinates, we set the option in setLowerOrderGeometryType
geometry_data.setLowerOrderGeometryType("coordinates")
# We want a straight line
geometry_data.setCreateMethod("straight")

# Now we add the start and end coordinates
geometry_data.addCoords(0.0, 3.0, 0.0)
geometry_data.addCoords(3.0, 3.0, 0.0)

# Now we instruct the database to the create the line. It will return an IFObject set containing the newly created line
object_set:'IFObjectSet' = lusas.database().createLine(geometry_data)

# Get all points from the returned object set
lines:list['IFLine'] = object_set.getObjects("Line")

# Loop through the lines and print their ids and coordinates
for line in lines:
    p1 = line.getStartPoint()
    p2 = line.getEndPoint()
    print(f"Line:{line.getID()} between points ({p1.getX()},{p1.getY()},{p1.getZ()}) to ({p2.getX()},{p2.getY()},{p2.getZ()}) ")


######################################################
### Arc line by coordinates

# The options and settings for creating all geometry in LUSAS is defined in the IFGeometryData object.
# To start any geometry creation, get the geometryData object and set all the defaults
geometry_data = lusas.geometryData().setAllDefaults()
# Here we are creating a line by specifying the coordinates, we set the option in setLowerOrderGeometryType
geometry_data.setLowerOrderGeometryType("coordinates")
# We want an arc
geometry_data.setCreateMethod("arc")
# Specify how we are supplying the coordinates, i.e Start->Middle->End
geometry_data.setStartMiddleEnd()

# Now we add the start, middle and end coordinates
geometry_data.addCoords(0.0, 4.0, 0.0)
geometry_data.addCoords(2, 5.0, 0.0)
geometry_data.addCoords(4.0, 4.0, 0.0)

# Now we instruct the database to the create the line. It will return an IFObject set containing the newly created line
object_set:'IFObjectSet' = lusas.database().createLine(geometry_data)

# Get all points from the returned object set
lines:list['IFLine'] = object_set.getObjects("Line")

# Loop through the lines and print their ids and coordinates
for line in lines:
    p1 = line.getStartPoint()
    p2 = line.getEndPoint()
    print(f"Line:{line.getID()}, length:{line.getLineLength()} between points ({p1.getX()},{p1.getY()},{p1.getZ()}) to ({p2.getX()},{p2.getY()},{p2.getZ()}) ")


######################################################
### Circle

radius = 6
z = 3.5
# The options and settings for creating all geometry in LUSAS is defined in the IFGeometryData object.
# To start any geometry creation, get the geometryData object and set all the defaults
geometry_data = lusas.geometryData().setAllDefaults()
# Specify the line by coordinate input
geometry_data.setLowerOrderGeometryType("coordinates")
# Specify defining a circle
geometry_data.makeCircle()
# Specify the meaning of the following coordinates 
geometry_data.setStartEndCentre()

# Start point at X=radius
geometry_data.addCoords(radius, 0.0, z)
# Specify the plane (X/Y)
geometry_data.addCoords(0.0, 1.0, z)
# Centre of the circle at the origin
geometry_data.addCoords(0.0, 0.0, z)

# Create the line in the database with the settings specified.
object_set:'IFObjectSet' = lusas.database().createLine(geometry_data)


######################################################
### Line from points

# Existing points can also be used to create lines.
# This can be done adding the start and end points in an IFObjectSet.
point1 = lusas.db().getObject("point", 1) #assumes point with ID 1 exists

# geometryData object contains all the settings to perform a geometry creation
geometry_data = lusas.geometryData().setAllDefaults()        
# set the options for creating straight lines from points
geometry_data.setCreateMethod("straight")
geometry_data.setLowerOrderGeometryType("points")
# Create an object set to contain the points and use this set to create the line
obs = lusas.newObjectSet()

# Add existing points to the object set
obs.add(point1) # Add first point (using point Object)
obs.add("point", 2) # Add second point (using point ID, assumes point with ID 2 exists)

# Create the line, get the line objects array from the returned object set and return the 1 and only line
new_line:IFLine = obs.createLine(geometry_data).getObjects("Line")


######################################################
### Line from Point translational sweep

# Create a point
point1 = lusas.db().getObject("point", 1) #assumes point with ID 1 exists
point2 = lusas.db().getObject("point", 2) #assumes point with ID 2 exists

# sweep vector x, y, z
vector = [1, 0, 0] 

# Create a translation attribute
attr = lusas.db().createTranslationTransAttr("Temp_SweepTranslation", vector)
attr.setSweepType("straight")
attr.setHofType("Line") # Set target geometry

geomData = lusas.newGeometryData()
geomData.setMaximumDimension(1) # Target geometries (0: Points, 1: Lines, 2: Surfaces)
geomData.setTransformation(attr)
geomData.sweptArcType("straight")

# Create an object set to contain the points and be swept
obs = lusas.newObjectSet()                 
obs.add(point1)
obs.add(point2)

# Perform the sweep, the returned object set will contain the created lines
objSet = obs.sweep(geomData)

# Delete the translation attribute
lusas.db().deleteAttribute(attr)

# Print new line IDs
newLines : list[IFLine] = objSet.getObjects("Lines")
for line in newLines:
    print(f"Line {line.getID()} created from sweep.")


######################################################
### Using Helper function
# The Helper module contains some useful functions to simplify the geometry creation process.

# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)

# Points creation:
point1 = Helpers.create_point(2.0, 1.0, 0.0)
point2 = Helpers.create_point(3.0, 2.0, 0.0)

# Lines creation:
line1 = Helpers.create_line_from_points(point1, point2)
line2 = Helpers.create_line_by_coordinates(0, 0, 0, 1, 1, 0)

# Lines creation by sweeps:
lines1 = Helpers.sweep_points([point1, point2], [1, 0, 0])
lines2 = Helpers.sweep_points_rotationally([point1, point2], 45) # 45 degrees
