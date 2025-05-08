# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      04c_Create_and_assign_loads.py
# Description:  Creates and assigns loads in the running LUSAS model
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
## Create Point load

Fx = 0.0 # Load in X direction
Fy = 0.0 # Load in Y direction
Fz = -100.0 # Load in Z direction (negative value = downwards)
Mx = 0.0 # Moment about X axis
My = 0.0 # Moment about Y axis
Mz = 0.0 # Moment about Z axis

pointLoadAttr = database.createLoadingConcentrated("Example Vertical Point Load")
pointLoadAttr.setConcentrated(Fx, Fy, Fz, Mx, My, Mz)

# Assign on all column top points for loadcase 1
pointLoadAttr.assignTo(topPoints, 1)


######################################################
## Create Distributes load

distrType = "Area" # Load distribution type: "Total" for total load, "Length" for length distribution, "Area" for area distribution
wx = 0.0 # Load in X direction
wy = 0.0 # Load in Y direction
wz = -100.0 # Load in Z direction (negative value = downwards)

distrLoadAttr = database.createLoadingGlobalDistributed("GlbD2")
distrLoadAttr.setGlobalDistributed(distrType, wx, wy, wz)

# Assign on slab for loadcase 1
pointLoadAttr.assignTo(surfPoints, 1)


######################################################
## Create/Assign mesh so that loads are visualised

database.createMeshLine("Dummy Line Mesh").setSize("BMI21", 1).assignTo(lines, 1)
database.createMeshSurface("Dummy Surface Mesh").setRegular("QTS4", 0, 0, True).assignTo(surface1, 1)
database.updateMesh()
