# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      13_Create_and_assign_supports.py
# Description:  Creates and assigns supports in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Initialise
Helpers.initialise(lusas) # Initialise the Helpers module
database = lusas.db() # Save database in variable

######################################################
## Create slab and columns to use in this example

# Create slab-surface
xs = [0, 5, 5, 0]
ys = [0, 0, 3, 3]
zs = [0, 0, 0, 0]
surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)

# Create columns-lines
surfPoints : list['IFPoint'] = lusas.newObjectSet().add(surface1).addLOF("Points").getObjects("Point")
lines : list['IFLine'] = Helpers.sweep_points(surfPoints, [0, 0, 3])
# Get the top points of the columns
topPoints : list['IFPoint'] = [ln.getEndPoint() for ln in lines]


######################################################
## Create Fixed support

attr = database.createSupportStructural("Fixed")
# Restrict all degrees of freedom
attr.setStructural("R", "R", "R", "R", "R", "R")  # R=Restrained

# Assign on slab points and loadcase 1
attr.assignTo(surfPoints, 1)


######################################################
## Create pinned support

attr = database.createSupportStructural("Pinned")
# Release all rotational degrees of freedom
attr.setStructural("R", "R", "R", "F", "F", "F")  # F=Free, R=Restrained

# Assign on column top points and loadcase 1
attr.assignTo(topPoints, 1)


######################################################
## Create translation springs support

attr = database.createSupportStructural("Springs")
# Mark translational degrees of freedoms as strings
attr.setStructural("S", "S", "S", "F", "F", "F")
# Set springs stiffness (in model units)
sType = "Area" # Spring stiffness distribution: "Total" for total stiffness, "Length" for length distribution, "Area" for area distribution
attr.setSpring(sType, 200, 200, 200, 0, 0, 0, 0, 0, 0)

# Assign on surface and loadcase 1
attr.assignTo(surface1, 1)


######################################################
## Create/Assign mesh so that supports are visualised

database.createMeshLine("Dummy Line Mesh").setSize("BMI21", 1).assignTo(lines, 1)
database.createMeshSurface("Dummy Surface Mesh").setRegular("QTS4", 0, 0, True).assignTo(surface1, 1)
database.updateMesh()
