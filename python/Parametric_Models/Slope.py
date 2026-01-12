# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      503 Slope.py
# Author:       Finite Element Analysis Ltd
# Description: Generates the geometry, assign all attributes.
    # Users can modify the number of slopes and the total height of the model (this will affect the other inputs)
    # Users are required to input the model geometry, including slope angles, heights of individual slopes, bench widths, crest width, and toe width.
    # The provided inputs have not been checked for validity.
    # The MC model is adopted for soil behaviour.
#######################################################################

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

import time
import math
import os
#######################################################################
# DIMENSION INPUTS - Edit these values directly in the editor
#######################################################################

# Clear console for clean output
os.system('cls' if os.name == 'nt' else 'clear')

#######################################################################
# USER INPUTS
#######################################################################

numberOfSlopes = 1   # Number of slopes, number of benches is numberOfSlopes-1
total_height = 15
###################

slopes = []          # Slopes in degree
benches = []         # Benches in meter
heights = []         # Heights in meter

print("=" * 60)
print("SLOPE STABILITY MODEL-INPUT PARAMETERS")
print("=" * 60)

for i in range(numberOfSlopes):
    value = float(input(f"Enter slope {i + 1} angle (degrees): "))
    slopes.append(value)

print()
for i in range(numberOfSlopes):
    value = float(input(f"Enter height {i + 1} (meters): "))
    heights.append(value)

print()
for i in range(numberOfSlopes - 1):
    value = float(input(f"Enter width of bench {i + 1} (meters): "))
    benches.append(value)

print()
# Additional dimensions
crest = float(input("Enter crest width (meters): "))
toe = float(input("Enter toe width (meters): "))

#######################################################################
# CALCULATE GEOMETRY
#######################################################################

# Calculate horizontal widths for each slope segment
widths = []
for h, s in zip(heights, slopes):
    w = h / math.tan(math.radians(s))
    widths.append(w)

total_width = crest + sum(widths) + sum(benches) + toe

print("\n" + "=" * 60)
print("CALCULATED GEOMETRY")
print("=" * 60)
print(f"Total height: {total_height:.2f} m")
print(f"Total width: {total_width:.2f} m")
print(f"Individual slope widths: {[f'{w:.2f}' for w in widths]}")
print("=" * 60)

#######################################################################
# LUSAS MODEL CREATION
#######################################################################

print("\nStarting model creation process...")

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Check if a model is open and not saved
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("Save or close the current model before running this code")

# Create a new model
filename = "slope_stability_model.mdl"
lusas.newProject("Structural", filename)

# Get a reference to the model database
database = lusas.getDatabase()
lusas.setVisible(True)
lusas.enableUI(True)
    
# Maximize LUSAS window and keep it on top
time.sleep(5)  # Give LUSAS a moment to appear

# Set the analysis category & vertical axis
database.setAnalysisCategory("2D Inplane")
database.setVerticalDir("Y")

# Set the unit system
database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))

# Initialise the Helpers module
Helpers.initialise(lusas)  

print("Creating surfaces...")

#######################################################################
# CREATE COORDINATES FOR SLOPE PROFILE
#######################################################################

xs = []
ys = []
zs = []

# Start at bottom left corner
xs.append(0.0)
ys.append(0.0)
zs.append(0.0)

# Go up to top left (full height)
xs.append(0.0)
ys.append(total_height)
zs.append(0.0)

# Crest (horizontal at top)
xs.append(crest)
ys.append(total_height)
zs.append(0.0)

# Build the slope profile from top down
current_x = crest
current_y = total_height

for i in range(numberOfSlopes):
    # Go down the slope by heights[i]
    current_x += widths[i]
    current_y -= heights[i]
    
    xs.append(current_x)
    ys.append(current_y)
    zs.append(0.0)
    
    # Add bench if not the last slope
    if i < numberOfSlopes - 1:
        current_x += benches[i]
        xs.append(current_x)
        ys.append(current_y)
        zs.append(0.0)

# Toe (horizontal at the current y level)
xs.append(current_x + toe)
ys.append(current_y)  # Stay at current y level (not 0)
zs.append(0.0)

# Drop down to ground level
xs.append(current_x + toe)
ys.append(0.0)  # Now drop to ground level
zs.append(0.0)

# Print coordinates for verification
print("\n" + "=" * 60)
print("SLOPE PROFILE COORDINATES")
print("=" * 60)
for i, (x, y) in enumerate(zip(xs, ys)):
    print(f"Point {i}: X = {x:.2f} m, Y = {y:.2f} m")
print("=" * 60)

# Create surface
surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)
print(f"\nMain soil surface {surface1.getID()} created successfully!")

# Meshing ##########################################
print("Creating surface mesh...")
# Create Surface (shell) mesh
surfMeshAttr = database.createMeshSurface("Shell Mesh")
surfMeshAttr.setIrregular("QPN8", 1)
# Assign the mesh to the surface on loadcase 1
surfMeshAttr.assignTo([surface1], 1)

# Update the mesh to apply the changes
print("Updating mesh...")
database.updateMesh()
# End meshing ###########################

# Supports ##############################
print("Creating support attributes...")
# Base is supported vertically and horizontally
fix_xy_support_attr = database.createSupportStructural("FixXY").setStructural("R", "R", "F", "F", "F", "F", "F", "F", "C", "F")
# Sides are supported horizontally
fix_x_support_attr = database.createSupportStructural("FixX").setStructural("R", "F", "F", "F", "F", "F", "F", "F", "C", "F")

# Assign support attributes
surfLines1 = lusas.newObjectSet().add(surface1).addLOF("Lines").getObjects("Line")
for i, line in enumerate(surfLines1):
    if line.getStartPoint().getY() == 0.0 and line.getEndPoint().getY()== 0.0:
        fix_xy_support_attr.assignTo (line,1) 
    elif line.getStartPoint().getX() == 0.0 and line.getEndPoint().getX()== 0.0:
        fix_x_support_attr.assignTo(line,1)
    elif line.getStartPoint().getX() >= total_width and line.getEndPoint().getX()>= total_width:
        fix_x_support_attr.assignTo(line,1) 
# End of supports ############################        

# Materials ##################################
print("Creating soil material...")
# Material attribute - Soil
soil_name = "Soil"
E_mod = 35e3            # Young's modulus
nu = 0.3                # Poisson's ratio
density = 2             # Density
alpha = 0.000012        # Coefficient of thermal expansion
friction = 38           # Friction angle
dilatancy = 8           # Dilatancy angle
dmpfactor = 0
cohesion = 10           # Cohesion
#K0 = 0.384              # Coefficient of earth pressure

material_attr = database.createIsotropicMaterial(soil_name, E_mod, nu, density)
material_attr.setValue("alpha", alpha)
material_attr.addPlasticModifiedMohrCoulomb("No", friction, dilatancy, 0, dmpfactor)
material_attr.addModifiedMohrCoulombCohesion(0, cohesion)

# Assign material to the surfaces on loadcase 1
material_attr.assignTo([surface1], 1)       
# End of Material #################################

# Loading ##############################
print("Creating loading attributes...")
# Create Distributed load
distrType = "Length"    # Load distribution
wx = 0.0                # Load in X direction
wy = -10.0              # Load in Y direction

distrLoadAttr = database.createLoadingGlobalDistributed("GlbD2")
distrLoadAttr.setGlobalDistributed(distrType, wx, wy)

# Assignment
distrLoadAttr.assignTo(surfLines1[1], 1)
# End of loading ########################

# Setup initial loadcase
print("Setting up initial loadcase...")
initial_loadcase: 'IFLoadcase' = database.getLoadset("Loadcase 1", 0)
initial_loadcase.addGravity(True)
initial_loadcase.setGravityFactor(1.0)
initial_loadcase.setTransientControl(0)
initial_loadcase.getTransientControl().setNonlinearManual().setOutput().setConstants()
initial_loadcase.getTransientControl().setValue("dlnorm",0.1).setValue("dtnrml",0.1) # Displacement norms

# Save the model before starting analysis
print("Saving model...")
lusas.getProject().save()

print("Model setup completed successfully!")