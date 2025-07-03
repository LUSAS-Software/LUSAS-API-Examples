# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      07_Get_Existing_Geometries.py
# Description:  Use ObjectSets (Database, Groups, Selection etc) and filter geometries
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Import Helpers module (which contains some useful functions)
import shared.Helpers as Helpers


# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Initialise Helpers
Helpers.initialise(lusas)


##############################################################################
# Create geometries for testing

Helpers.create_point(2.0, 1.0, 0.0)
Helpers.create_line_by_coordinates(0, 0, -1, 1, 0, -1)
surf = Helpers.create_surface_by_coordinates([0,1,1,0], [0,0,1,1], [0,0,0,0])
Helpers.sweep_surfaces([surf], [0, 0, 1])


##############################################################################
# Access existing geometries

# Get model database (which is a special type of IFObjectSet)
object_set = lusas.db()

# Get all nodes
nodes : list[IFNode] = object_set.getObjects("Nodes")

# Get all elements
elements : list[IFElement] = object_set.getObjects("Elements")

# Get all points
points : list[IFPoint] = object_set.getObjects("Points")

# Get all lines
lines : list[IFLine] = object_set.getObjects("Lines")

# Get all surface
surfaces : list[IFSurface] = object_set.getObjects("Surfaces")

# Get all volumes
volumes : list[IFVolume] = object_set.getObjects("Volumes")

# Print number of geometries
print(f"The model contains:")
print(f" - {object_set.count("Nodes")} Nodes")
print(f" - {object_set.count("Elements")} Elements")
print(f" - {object_set.count("Points")} Points")
print(f" - {object_set.count("Lines")} Lines")
print(f" - {object_set.count("Surfaces")} Surfaces")
print(f" - {object_set.count("Volumes")} Volumes")

# Get features by ID
if lusas.db().exists("point", 1):
    print(f"Point 1 exists!")
    point1 = lusas.db().getObject("point", 1)
else:
    print(f"Point 1 does not exist!")


##############################################################################
# Set of features (object sets)

# Create a new object set
new_object_set = lusas.newObjectSet()

if len(points) > 0:
    # Add points in the object set
    new_object_set.add(points)
    # But remove the first
    new_object_set.remove(points[0])

print(f"The new object set now contains {new_object_set.count("Points")} / {len(points)} Points")


# Object sets can also be used to access lower or higher order geometries (e.g. the lines of a surface, or the volumes that contain the included surfaces).

# Add higher order Line feature (the lines using the object set contained points)
new_object_set.addHOF("Lines")

print(f"The new object set now contains {new_object_set.count("Points")} Points and {new_object_set.count("Lines")}  Lines")

# Keep only the lines
new_object_set.keep("Lines")
print(f"The new object set now contains {new_object_set.count("Points")} Points and {new_object_set.count("Lines")}  Lines")

# Add lower order Point features (points of included lines)
new_object_set.addLOF("Points")
print(f"The new object set now contains {new_object_set.count("Points")} Points and {new_object_set.count("Lines")}  Lines")


##############################################################################
# Groups

# Create an empty group
groupVlms = lusas.db().createEmptyGroup("Volumes")

# Add volumes in the group (groups are special types of object sets, so they share the same methods)
groupVlms.add(volumes)
print(f"Group Volumes now contains {groupVlms.count("all")} feature(s)")

# Create group with features in one line
groupSurfaces = lusas.db().createGroup("Surfaces", surfaces)
print(f"Group Surfaces now contains {groupSurfaces.count("all")} feature(s)")

# Add relevant points in the surfaces group
groupSurfaces.addLOF("Points")
print(f"Group Surfaces now contains {groupSurfaces.count("all")} feature(s)")

# Now remove all points from the Surfaces group
groupSurfaces.remove("Points")
print(f"Group Surfaces now contains {groupSurfaces.count("all")} feature(s)")


##############################################################################
# Selection

# Ensure selection is empty (which is also an object set!)
lusas.selection().remove("all")

# Add all points to selection
lusas.selection().add(lusas.db().getObjects("Points"))

# Print number of selected features
print(f"Selection contains {lusas.selection().count("all")} feature(s)")


##############################################################################
# Geometry filtering - Get volume top points example

# 1. Get all volume points by adding it in an objectSet
t_object_set = lusas.newObjectSet().add(volumes[0]).addLOF("Points")
volumePoints : list[IFPoint] = t_object_set.getObjects("Points")

# 2. Print points info
print("Volume points:")
for point in volumePoints:
    print(f" - ID: {point.getID()}, x: {point.getX()}, y: {point.getY()}, z: {point.getZ()}")

# 3. Get max Z coordinate
zs = [p.getZ() for p in volumePoints]
maxZ = max(zs)
print(f"Max Z: {maxZ}")

# 4. Get all points close to max Z (geometric comparison should always be done base on a tolerance)
tolerance = 0.000001
topPoints = []
print("Top volume points:")
for point in volumePoints:
    # Check if close to top
    if abs(point.getZ() - maxZ) > tolerance:
        continue
    # Add point in the list
    topPoints.append(point)
    print(f" - ID: {point.getID()}, x: {point.getX()}, y: {point.getY()}, z: {point.getZ()}")

# 5. Select top points
lusas.selection().remove("all")
if len(topPoints) > 0:
    lusas.selection().add(topPoints)
