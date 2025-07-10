# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      10_Create_and_assign_mesh.py
# Description:  Creates and assigns meshes in the running LUSAS model
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Initialise
Helpers.initialise(lusas) # Initialise the Helpers module
database = lusas.db() # Save database in variable


######################################################
## Create line and surface to use in this example

# Create line
line1 = Helpers.create_line_by_coordinates(0.0, 3.0, 0.0, 3.0, 3.0, 0.0)
# To get existing line, use the following command instead:
# line1 = database.getObject("line", 1) #get line with ID 1

# Create vertical surface
surface1 = Helpers.sweep_lines([line1], [0, 0, 1])
# To get existing surface, use the following command instead:
# surface1 = database.getObject("surface", 1) #get surface with ID 1


######################################################
## Create Line (beam) mesh
lineMeshAttr = database.createMeshLine("Beam Mesh")

# Set the element type and size of elements BMI21 = 2Node thick beam elements, 1 = 1m length (set model units)
lineMeshAttr.setSize("BMI21", 1)

# Assign the mesh to the line on loadcase 1
lineMeshAttr.assignTo(line1, 1)


######################################################
## Create Surface (shell) mesh
surfMeshAttr = database.createMeshSurface("Shell Mesh")
# Set the element type and divisions of elements QTS4 = 4Node quadrilateral surface elements
# 0 divisions in the u and v directions for automatic meshing
surfMeshAttr.setRegular("QTS4", 0, 0, True)

# Assign the mesh to the surface on loadcase 1
surfMeshAttr.assignTo(surface1, 1)


######################################################
# Update the mesh to apply the changes
database.updateMesh()
