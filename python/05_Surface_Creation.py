# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      05_Surface_Creation.py
# Description:  Creates surfaces in the running LUSAS model
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.database()


######################################################
#### Create a Surface by coordinates

# Create a geometryData object to contain all the settings for the geometry creation
geometry_data = lusas.newGeometryData()
# set the options for creating geometries from coordinates
geometry_data.setCreateMethod("coons")
geometry_data.setLowerOrderGeometryType("coordinates")

# Specify surface coordinates
geometry_data.addCoords(0, 0, 0)
geometry_data.addCoords(1, 0, 0)
geometry_data.addCoords(1, 1, 0)
geometry_data.addCoords(0, 1, 0)

surface1 : IFSurface = database.createSurface(geometry_data).getObjects("Surface")[0]
print(f"Surface {surface1.getID()} created by coordinates.")

######################################################
#### Create a Surface by Lines (copy lines from previously created surface)


# Get the perimeter lines of the created surface
# (add surface in ObjectSet, add Lower Order Line Features in the set, then keep only lines in the set)
objSet = lusas.newObjectSet().add(surface1).addLOF("Line").keep("Line")

## Copy the lines by 1m in Z direction
vector = [0, 0, 1]
# Create a translation attribute
transform = database.createTranslationTransAttr("Trn1", vector)
# Create a geometryData object to contain all the settings for the copy
geometry_data = lusas.newGeometryData()
geometry_data.setAllDefaults()
geometry_data.setTransformation(transform)
# Copy the lines
linesObj = objSet.copy(geometry_data).keep("Line")
# Delete the translation attribute
database.deleteAttribute(transform)

## Create a surface from the lines
# Reset the geometryData object that will contain all the settings for the geometry creation
geometry_data.setAllDefaults()
# set the options for creating geometries from lines
geometry_data.setCreateMethod("coons")
geometry_data.setLowerOrderGeometryType("lines")

# Create the surface using the lines
new_surface : IFSurface = linesObj.createSurface(geometry_data).getObjects("Surface")[0]
print(f"Surface {new_surface.getID()} created by lines.")


######################################################
#### Surface from Line translational sweep

# Create a point
line1 = database.getObject("line", 1) #assumes line with ID 1 exists

# sweep vector X, Y, Z
vector = [0, 0, 1] # 1m at Z direction

# Create a translation attribute
attr = database.createTranslationTransAttr("Temp_SweepTranslation", vector)
attr.setSweepType("straight")
attr.setHofType("Surface") # Set target geometry

geomData = lusas.newGeometryData()
geomData.setMaximumDimension(2) # Target geometries (0: Points, 1: Lines, 2: Surfaces)
geomData.setTransformation(attr)
geomData.sweptArcType("straight")

# Create an object set to contain the points and be swept
obs = lusas.newObjectSet().add(line1)

# Perform the sweep, the returned object set will contain the created surfaces
objSet = obs.sweep(geomData)

# Delete the translation attribute
database.deleteAttribute(attr)

# Print new line IDs
newSurfaces : list[IFSurface] = objSet.getObjects("Surface")
for surface in newSurfaces:
    print(f"Surface {surface.getID()} created from sweep.")


######################################################
### Using Helper function
# The Helper module contains some useful functions to simplify the geometry creation process.

# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)

# Surface creation by coordinates:
xs = [0.0, 1, 1, 0]
ys = [1.0, 1, 1, 1]
zs = [0, 0, 1, 1]
surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)
print(f"Surface {surface1.getID()} created by coordinates (using helpers).")

# Lines creation by coordinates:
line1 = Helpers.create_line_by_coordinates(1, 0, 0, 2, 0, 0)
print(f"Line {line1.getID()} created by coordinates (using helpers).")

# Surface creation by sweeps:
surfaces1 = Helpers.sweep_lines([line1], [0, 1, 0])
for surface in surfaces1:
    print(f"Surface {surface.getID()} created by sweep (using helpers).")

surfaces2 = Helpers.sweep_lines_rotationally([line1], -90, [1, 0, 0], "y") # -90 degrees around Y axis
for surface in surfaces1:
    print(f"Surface {surface.getID()} created by rotational sweep (using helpers).")

# Set isometric view (top side view) and fit view
lusas.view().setIsometric()
lusas.view().setScaledToFit(True)
