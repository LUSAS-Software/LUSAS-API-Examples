# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      11_Create_and_assign_section.py
# Description:  Creates and assigns a section in the running LUSAS model
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
## Geometric Line (beam) section using the section library

# Create a geometric attribute object
beamSection = database.createGeometricLine("Geometric Line from Library")
# Set the element type
beamSection.setValue("elementType", "3D Thick Beam")

# Set section from library (library name, library type, section name, as shown in the LUSAS GUI)
sectionNo = 0 # 0 for first section (uniform if no other sections are defined)
rotation = 1 # Rotation of the section about the local x-axis (1 = 90 degrees)
beamSection.setFromLibrary("UK Sections", "Universal Beams (BS4)", "305x165x46kg UB", rotation, 0, sectionNo)

# Assign the mesh to the line on loadcase 1
beamSection.assignTo(line1, 1)


######################################################
## Geometric Line (beam) section with custom properties

# Create a geometric attribute object
customSection = database.createGeometricLine("Geometric Line from Properties")
# Set the element type
customSection.setValue("elementType", "3D Thick Beam")

# Set custom properties (in model units)
Area = 5.87461E-3 # Cross-sectional area
Iyy = 98.9866E-6 # Moment of inertia about the y-axis
Izz = 8.95665E-6 # Moment of inertia about the z-axis
Iyz = 0.0 # Product of inertia about the y and z axes
J_const = 0.224843E-6 # Torsional constant
Asz = 3.39835E-3 # Shear area about the z-axis
Asy = 1.97516E-3 # Shear area about the y-axis
ey = 0.0 # Distance from the centroid to the top of the section in the y-direction
ez = 0.0 # Distance from the centroid to the top of the section in the z-direction
sectionNo = 0 # 0 for first section (uniform if no other sections are defined)
customSection.setBeam(Area, Iyy, Izz, Iyz, J_const, Asz, Asy, ey, ez, sectionNo)

# To assign the mesh to the line on loadcase 1, the following command could be used
# customSection.assignTo(line1, 1)


######################################################
## Geometric Line (beam) section with parametric section

# Create the Rectangular Solid Section (utility)
rectSection = database.createParametricSection("Sct1")
rectSection.setType("Rectangular Solid")
# Set the section properties (in model units) - breath 0.4 and depth 0.6
names = ["B", "D"]
values = [0.4, 0.6]
rectSection.setDimensions(names, values)

# Create a geometric attribute object and set the parametric section
paramSection = database.createGeometricLine("LGeo1")
paramSection.setValue("elementType", "3D Thick Beam")
paramSection.setFromLibrary("Utilities", "", "Sct1", 0, 0, 0)

# To assign the mesh to the line on loadcase 1, the following command could be used
# paramSection.assignTo(line1, 1)


######################################################
## Surface thickness

# Create a geometric attribute object
thicknessAttr = database.createGeometricSurface("Thickness")
# Set thickness and eccentricity (in model units)
t = 0.1 # Thickness
ec = 0.0 # Eccentricity
thicknessAttr.setSurface(t, ec)

# Assign thickness to the surface on loadcase 1
thicknessAttr.assignTo(surface1, 1)


######################################################
## Create/Assign mesh and enable fleshing to draw sections

database.createMeshLine("Dummy Line Mesh").setSize("BMI21", 1).assignTo(line1, 1)
database.createMeshSurface("Dummy Surface Mesh").setRegular("QTS4", 0, 0, True).assignTo(surface1, 1)
database.updateMesh()

lusas.view().attributes().setVisible(True)
lusas.view().attributes().setDrawStyle("Geometric", "Arrows")
lusas.view().attributes().visualiseAll("Geometric")
