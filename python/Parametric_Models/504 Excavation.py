# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      504 Excavation.py
# Author:       Finite Element Analysis Ltd
# Description:  Generates the geometry, assigns all attributes, and creates construction stages.
#               Users can edit geometry inputs.
#               The MC model is adopted for soil behaviour.
#               Interfaces are taken into consideration.
#######################################################################

# Add parent directory to sys.path so that we can load libraries from the parent directory
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(parent_dir)


# Libraries:
import math
from win32com.client import CastTo
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

import numpy as np
import pandas as pd

# Clear console for clean output
os.system('cls' if os.name == 'nt' else 'clear')
print("Starting model creation...")

#######################################################################
# INITIALIZE MODEL
#######################################################################

# Get LUSAS modeller instance
lusas = get_lusas_modeller()

# Safety check: prevent overwriting unsaved work
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("Please save or close the current model before running.")

# Create new project and get database reference
lusas.newProject("Structural", "Excavation.mdl")
database = lusas.getDatabase()
lusas.setVisible(True)
lusas.enableUI(True)

# Set global analysis parameters
database.setAnalysisCategory("2D Inplane")
database.setVerticalDir("Y")
database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))
database.setTimescaleUnits("Days")
Helpers.initialise(lusas)

# Inputs
soil_layers = [3, 12, 5]
wall_depth = 15
water_level = 3

excavation_depths = [3, 4, 3]
width_excavation = 10
width_retained   = 30

spacing_of_anchors = 3 # Anchor stiffness will be reduced to reflect this spacing (m)

# (index, angle from vert, length, grout length, load)
# Anchors are indexed from the excavation levels
anchors : 'list[tuple[int, float, float, float, float]]' = [(0, 56, 11, 3.5, 120), (2, 45, 6, 4, 200)]

bar_area = 7.07e-4
grout_area = 0.28
wall_thickness = 0.35

mesh_size = 1.0

surcharge_offset = 2 # back from wall (m)
surcharge_length = 5 # meter
surcharge_intensity = 10 #kpa

# Checking parameters
assert wall_depth > sum(excavation_depths),       "The wall depth should be larger than the excavation"
assert wall_depth < sum(soil_layers),             "The wall depth should be smaller than the total depth of soil layers"
assert sum(soil_layers) > sum(excavation_depths), "The total depth of soil layers should be larger than the excavation"
assert water_level == excavation_depths[0],       "The first excavation is assumed to be down to the level of the water table"

embed_length = wall_depth - sum(excavation_depths)
soil_depth = sum(soil_layers)

# Mesh
# Two-phase plane strain quadrilateral elements are used for the soil
soil_mesh_attr         = database.createMeshSurface("Soil").setIrregular("QPN8P", mesh_size )
# Two-phase interface elements to model Mohr=Coulomb friction contact between the structure and soil
interface_mesh_attr    = database.createMeshLine("Interface").setSize("IPN6P", mesh_size )
# Plane strain beam elements for the wall
wall_mesh_attr         = database.createMeshLine("Wall").setSize("BMI3N", mesh_size )
# Single bar element for anchor rods
anchor_bar_mesh_attr   = database.createMeshLine("Anchor Bar").setNumber("BAR2", 1 )
# Quadratic bar elements for the anchor grout to match the plane strain soil mesh
anchor_grout_mesh_attr = database.createMeshLine("Anchor Grout").setSize("BAR3", mesh_size )

# Geometric
# Thickness for plane strain beam elements
wall_geom_attr         = database.createGeometricLine("Wall").setElementType("Plane Strain Beam").setPlaneStrain(wall_thickness)
# Bar areas for the anchor bars
anchor_bar_geom_attr   = database.createGeometricLine("Anchor Bar").setElementType("Bar/Link").setBeam(bar_area, 0,0,0,0,0,0)
anchor_grout_geom_attr = database.createGeometricLine("Anchor Grout").setElementType("Bar/Link").setBeam(grout_area, 0,0,0,0,0,0)

# Material
soil_material_attrs:list[IFAttribute] = []
# Read the soil material definitions from the corresponding spreadsheet
df_soils = pd.read_excel("510 Soil_Inputs.xlsx", header=1)
# First 3 columns define properties, remaining are soil material definitions
if len(df_soils.columns) > 3:
    for i in range(3, len(df_soils.columns)):
        # Name and parameters
        soil_name = df_soils.iloc[:,i].name
        params = dict(zip(df_soils.iloc[:,2], df_soils.iloc[:,i]))
        # Create the material
        attr = database.createIsotropicMaterial(soil_name, params['E'], params['nu'], params['rho'])
        # Modified Mohr-Coulomb properties with Rankine cut-off
        attr.addPlasticModifiedMohrCoulomb("Rankine", params['frc'], params['dil'], 0, params['dmpFct'])
        attr.addModifiedMohrCoulombCohesion(0, params['CSngle'])
        attr.addModifiedMohrCoulombTensile(0, params['QmaxSngle'])
        attr.addModifiedMohrCoulombCompressive(0, params['QminSngle'])
        # Two Phase
        attr.addConstantWaterContentTwoPhase(0.0, params['Kf'], params['n'], 9.81, params['kx'], params['ky'], params['kz'], 
                                             params['rhoF'], params['Swc'], params['Sws'], params['Kred'], 0.0, 
                                             "Absolute value", "saturation", "Fully saturated")
        # Ko Initialisation
        attr.addKoElasticRow(0.0, params['Ko'])
        soil_material_attrs.append(attr)

# Check we have sufficient soil materials defined for the number of layers
assert len(soil_material_attrs) >= len(soil_layers), " The number of defined soil materials is less than the defined layers"

# Elastic materials for the wall and anchors. Note anchors are reduced to account for horizontal spacing
wall_material_attr          = database.createIsotropicMaterial("Wall", 35e6, 0.15, 2.4)
anchor_bar_material_attr    = database.createIsotropicMaterial("Anchor rod", 200e6/spacing_of_anchors, 0.3, 0.0)
anchor_grout_material_attr  = database.createIsotropicMaterial("Anchor Grout", 250e6/spacing_of_anchors, 0.1, 0.0)

# Create an interface material for each of the soil materials
soil_interfaces:list[IFSoilStructureMaterialSet] = list()
for soil_attr in soil_material_attrs:
    interface_material_attr = database.createSoilStructureMaterialSet(f"wall/{soil_attr.getName()}")
    interface_material_attr.setSoilInterfaceGraphType("displacement")
    interface_material_attr.addSoilNrmInterfaceRow(10.0, 0.15, 0.0, 20.0, 0.0, 1.0, -1.0, 0.0)
    interface_material_attr.setSoilInterfacePropertiesType("Never")
    interface_material_attr.addTwoPhaseInterface(0.0)
    soil_interfaces.append(interface_material_attr)

# Water
# Phreatic mesh attributes defining the water levels in the model
# We have one for the initial water level and additional surface for each "de-watering" prior to excavation.
phreatic_mesh_attrs:list[IFMeshPhreatic] = [database.createMeshPhreatic("Groundwater")]
for i in range(1, len(excavation_depths)):
    phreatic_mesh_attrs.append(database.createMeshPhreatic(f"De-watering {i}"))

# Water pressure distribution loads defined from the phreatic surfaces
water_pressure_attrs:list[IFWaterPressureDistrLoad] = []
# Always have a ground water pressure
attr = database.createLoadingWaterPressureDistr("Groundwater pwp")
attr.setDensity(1.0).setOnlyPoreWaterPressure(True).setPhreatic(phreatic_mesh_attrs[0], "faces")
water_pressure_attrs.append(attr)
# Create additional pressures for each dewatering stage
for i in range(1, len(excavation_depths)):
    attr = database.createLoadingWaterPressureDistr(f"De-watering pwp {i}")
    attr.setDensity(1.0).setOnlyPoreWaterPressure(True).setPhreatic(phreatic_mesh_attrs[i], "faces")
    water_pressure_attrs.append(attr)

# Boundary conditions
# Base is supported vertically and horizontally
fix_xy_support_attr = database.createSupportStructural("FixXY").setStructural("R", "R", "F", "F", "F", "F", "F", "F", "C", "F")
# Sides are supported horizontally
fix_x_support_attr  = database.createSupportStructural("FixX") .setStructural("R", "F", "F", "F", "F", "F", "F", "F", "C", "F")

# Loading
# Surcharge loading is applied over a patch on the retained side.
# A variation is used to specify the extent of the load which is assigned to the whole line.
load_variation_attr = database.createVariationLine("Surcharge Limits")
load_variation_attr.setFunction("Actual")
load_variation_attr.addRowUnequal(0.0, 0.0)
load_variation_attr.addRowUnequal(surcharge_offset, 0.0)
load_variation_attr.addRowUnequal(surcharge_offset*1.001, 1.0)
load_variation_attr.addRowUnequal(surcharge_offset+surcharge_length, 1.0)
load_variation_attr.addRowUnequal(surcharge_offset+surcharge_length, 0.0)

# Surcharge loading is a face loading with intensity defined by the variation
surchage_load_attr = database.createLoadingFace(f"Surchage load {surcharge_intensity}kPa").setFace(0.0, f"{surcharge_intensity}*{load_variation_attr.getName()}", 0.0, 0.0)

# Dewatering is modelled by moving a phreactic surface using a prescribed displacement
dewater_load_attrs:list[IFAttribute] = []
for i, d in enumerate(excavation_depths[1:]):
    pd = database.createPrescribedDisplacementLoad(f"De-water {i+1}", "Total").setDisplacement("V", -d)
    dewater_load_attrs.append(pd)

# Anchorage loads are modelled using target stress-strains
anchor_load_attrs:list[IFAttribute] = []
for i, anchor in enumerate(anchors):
    anchor_load_attrs.append(database.createLoadingStressStrain(f"Anchor {i+1}={anchor[4]}kN").setStressStrain("Target", [anchor[4], "N/A"], "Line", "Bar", 2))

# Automatic loading is used to reduce the residual forces of the excavated soil. 
# A dummy load is used to replace the prescribed displacement in the automatic loading.
dummy_load_attr = database.createLoadingConcentrated("dummy load for excavation").setConcentrated(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

wall_activate_attr = database.createActivate("wall")
# Activate each or the anchors
anchor_activation_attrs:list[IFAttribute] = []
for i in range(len(anchors)):
    anchor_activation_attrs.append(database.createActivate(f"Activate Anchor {i+1}"))

structure_deactivate_attr = database.createDeactivate("wall and anchors").setDeactivate("custom", 100.0, 1.0E-6)
structure_deactivate_attr.setCustomType("activeMesh").setForceDistribution("distribute over stage")

excavation_deactivate_attrs:list[IFAttribute] = []
for i in range(len(excavation_depths)):
    attr = database.createDeactivate(f"Excavation {i+1}").setDeactivate("custom", 100.0, 1.0E-6)
    attr.setCustomType("activeMesh").setForceDistribution("distribute over stage")
    excavation_deactivate_attrs.append(attr)

# Vertical coordinates defined by soil layers
soil_coords = [soil_depth]+[soil_depth-float(y) for y in np.add.accumulate(soil_layers) ]
print("Soil coords : ", soil_coords)
# Vertical coordinates of each excavation depth
excv_coords = [soil_depth]+[soil_depth-float(y) for y in np.add.accumulate(excavation_depths) ]
print("Excavation coords : ", excv_coords)
# Combined vertical coordinates for soil layers and excavation depths
vertical_coords = list(set(soil_coords + excv_coords + [wall_depth, 0]))
vertical_coords.sort(reverse=True)
print("Vertical coords : ", vertical_coords)


# Coordinates of the wall
wall_coords     = [y for y in vertical_coords if y >= soil_depth-wall_depth]
print("Wall coords : ", wall_coords)
# Coordinates beneath the wall
sub_wall_coords = [y for y in vertical_coords if y < soil_depth-wall_depth]
print("Subwall coords : ", sub_wall_coords)

debug_offset = 0 # Use this to create interface lines with a gap so they can be checked

# Create the 3 overlapping lines, 1 for the wall and 1 for the soil interface eitherside. The wall will be connected to the soil with the interface elements
# wall_coords = [soil_depth]+[soil_depth-float(y) for y in np.add.accumulate( excavation_depths + [embed_length]) ]
# Prevent the features merging together
database.options().setBoolean("newFeaturesMergeable", False)
# Create the points
wall_points      = [Helpers.create_point(width_excavation, y, 0) for y in wall_coords]
retained_points  = [Helpers.create_point(width_excavation+debug_offset, y, 0) for y in wall_coords]
excavated_points = [Helpers.create_point(width_excavation-debug_offset, y, 0) for y in wall_coords]
# Join the points to form lines
wall_lines      = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(wall_points, wall_points[1:]) ]
retained_lines  = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(retained_points, retained_points[1:]) ]
excavated_lines = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(excavated_points, excavated_points[1:]) ]
database.options().setBoolean("newFeaturesMergeable", True)

if debug_offset > 0:
    lusas.newObjectSet().add(retained_points[-1]).modify(lusas.geometryData().setAllDefaults().modifyPosition(width_excavation, retained_points[-1].getY(), 0))
    lusas.newObjectSet().add(excavated_points[-1]).modify(lusas.geometryData().setAllDefaults().modifyPosition(width_excavation, excavated_points[-1].getY(), 0))

# Merge the points at the bottom of the wall
objs = lusas.newObjectSet().add(wall_points[-1]).add(retained_points[-1]).add(excavated_points[-1])
objs.makeMergeable(lusas.geometryData().setAllDefaults().setLowerOrderGeometryType("points"))
p = objs.getObject("Point")
# Cast to IFPoint to access getY() method
p = CastTo(p, "IFPoint")
# Merging points deletes them so we have to update our point references to the new point
wall_points[-1] = p
retained_points[-1] = p
excavated_points[-1] = p

# points and lines beneath the wall
sub_wall_points = [Helpers.create_point(width_excavation, y, 0) for y in sub_wall_coords]
sub_wall_lines = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip([wall_points[-1]]+sub_wall_points, sub_wall_points) ]

# Points at the boundaries of the problem
lhs_points    = [Helpers.create_point(0, y, 0) for y in vertical_coords]
rhs_points    = [Helpers.create_point(width_excavation + width_retained, y, 0) for y in vertical_coords]
# Lines at the boundaries
lhs_lines     = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(lhs_points, lhs_points[1:]) ]
rhs_lines     = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(rhs_points, rhs_points[1:]) ]
# Horizontal lines for the excavation layers
exc_hor_lines = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(lhs_points, excavated_points+sub_wall_points) ]
ret_hor_lines = [Helpers.create_line_from_points(p1, p2) for p1, p2 in zip(retained_points+sub_wall_points, rhs_points ) ]

# Surfaces on the excavated side
excavated_lines_all = excavated_lines + sub_wall_lines
excavated_surfaces:list[IFSurface] = []
for i in range(len(exc_hor_lines)-1):
    excavated_surfaces.append(Helpers.create_surface_from_lines([exc_hor_lines[i], excavated_lines_all[i], exc_hor_lines[i+1], lhs_lines[i]]))

# Surfaces on the retained side
retained_lines_all = retained_lines + sub_wall_lines
retained_surfaces:list[IFSurface] = []
for i in range(len(exc_hor_lines)-1):
    retained_surfaces.append(Helpers.create_surface_from_lines([ret_hor_lines[i], rhs_lines[i], ret_hor_lines[i+1], retained_lines_all[i]]))

# Anchorages
anchor_lines : 'list[tuple[IFLine, IFLine]]' = []
for i, angle, rod_length, grout_length, force in anchors:
    full_length = rod_length+grout_length
    theta = math.radians(angle)
    p1 = Helpers.create_point(width_excavation + rod_length  * math.sin(theta), wall_points[i+1].getY() - rod_length  * math.cos(theta), 0 )
    p2 = Helpers.create_point(width_excavation + full_length * math.sin(theta), wall_points[i+1].getY() - full_length * math.cos(theta), 0 )
    rod = Helpers.create_line_from_points(wall_points[i+1], p1)
    grout = Helpers.create_line_from_points(p1, p2)
    anchor_lines.append((rod, grout))

anchor_surfaces = []
if len(anchor_lines) > 0:
    for i in range(len(anchor_lines)-1):
        anchor_surfaces.append(Helpers.create_surface_from_points([
            anchor_lines[i][1].getStartPoint(), 
            anchor_lines[i][1].getEndPoint(),
            anchor_lines[i+1][1].getEndPoint(), 
            anchor_lines[i+1][1].getStartPoint()
        ]))


# Lines representing the phreatic surfaces
x = width_excavation + width_retained
line_ground_water = Helpers.create_line_by_coordinates(x+1, soil_depth-water_level, 0, x+3, soil_depth-water_level, 0)

line_water_levels = [line_ground_water]
depth = soil_depth
for excavation in excavation_depths[:-1]:
    depth-=excavation
    line = Helpers.create_line_by_coordinates(-3, depth, 0, -1, depth, 0)
    line_water_levels.append(line)

# Soil Mesh
soil_mesh_attr.assignTo(excavated_surfaces)
soil_mesh_attr.assignTo(anchor_surfaces)
soil_mesh_attr.assignTo(retained_surfaces)
# Anchor mesh
anchor_bar_mesh_attr.assignTo([l[0] for l in anchor_lines])
anchor_grout_mesh_attr.assignTo([l[1] for l in anchor_lines])
# Wall mesh
wall_mesh_attr.assignTo(wall_lines)
# Interface mesh
for i in range(len(wall_lines)):
    objs = lusas.newObjectSet().add(retained_lines[i]).add(wall_lines[i])
    interface_mesh_attr.assignTo(objs)
    objs = lusas.newObjectSet().add(excavated_lines[i]).add(wall_lines[i])
    interface_mesh_attr.assignTo(objs)
# Phreatic mesh assigned to each of the defined lines
for i, line in enumerate(line_water_levels):
    phreatic_mesh_attrs[i].assignTo(line_water_levels[i])

# Geometric assignments
wall_geom_attr.assignTo(wall_lines)
anchor_bar_geom_attr.assignTo([l[0] for l in anchor_lines])
anchor_grout_geom_attr.assignTo([l[1] for l in anchor_lines])

# Wall Material
wall_material_attr.assignTo(wall_lines)
anchor_bar_material_attr.assignTo([l[0] for l in anchor_lines])
anchor_grout_material_attr.assignTo([l[1] for l in anchor_lines])

# Soil materials and corresponding interface material
y = soil_depth
prev_i = 0
for i, depth in enumerate(soil_layers):
    y-=depth
    iy = vertical_coords.index(y)
    soil_material_attrs[i].assignTo(excavated_surfaces[prev_i:iy])
    soil_material_attrs[i].assignTo(retained_surfaces[prev_i:iy])
    # interface material for the corresponding soil attribute
    soil_interfaces[i].assignTo(excavated_lines[prev_i:iy])
    soil_interfaces[i].assignTo(retained_lines[prev_i:iy])
    prev_i = iy

# Support assignments
fix_x_support_attr.assignTo(lhs_lines)
fix_x_support_attr.assignTo(rhs_lines)
fix_xy_support_attr.assignTo(exc_hor_lines[-1])
fix_xy_support_attr.assignTo(ret_hor_lines[-1])

retained_surf_attr = database.createDesignAttribute("Retained", "Retained", "Retained", "surfaces")
retained_surf_attr.assignTo(retained_surfaces)

anchor_surf_attr = database.createDesignAttribute("Anchor", "Anchor", "Anchor", "surfaces")
anchor_surf_attr.assignTo(anchor_surfaces)

horiz_line_attr = database.createDesignAttribute("HorizLine", "HorizLine", "HorizLine", "lines")
horiz_line_attr.assignTo(ret_hor_lines)

anchor_line_attrs:list[IFDesignAttribute] = []
for i, lines in enumerate(anchor_lines):
    attr = database.createDesignAttribute(f"Anchor Line {i+1}", "Anchor", "Anchor", "lines")
    attr.assignTo(lines[1])
    anchor_line_attrs.append(attr)

geom_data = lusas.geometryData().setAllDefaults().useInDependents(True)

did_split = True
while did_split:
    for line in database.getObjects(horiz_line_attr):
        for anchor_surface in database.getObjects(anchor_surf_attr):    
            objs = lusas.newObjectSet().add(anchor_surface).add(line).splitSurface(geom_data)
            did_split = len(objs.getObjects("Surface"))> 0
            if did_split: break

did_split = True
while did_split:
    for surface in database.getObjects(anchor_surf_attr):

        for retained_surface in database.getObjects(retained_surf_attr):
            geom_data = lusas.geometryData().setAllDefaults()
            geom_data.setBooleanSimplify(False)
            geom_data.setBooleanDeletePrimary(False)
            # geom_data.setBooleanDeleteSecondary(False)
            geom_data.setBooleanReverseOrderOfSubtraction(True)
            objs = lusas.newObjectSet().add(surface).add(retained_surface)
            returned_objs = objs.booleanSubtraction(geom_data)
            did_split = len(returned_objs.getObjects("Surface"))> 0
            if did_split: break

# Helper function to get the soil material from the soil depth
def get_soil_index_from_depth(y:float) -> int:
    layer_level = soil_depth
    for i, d in enumerate(soil_layers):
        if y < layer_level and y > (layer_level-d): return i

# Assign the relevant soil material to each of the split surfaces in the anchorage zone
anchor_surfaces:list[IFSurface] = database.getObjects(anchor_surf_attr)
for surface in anchor_surfaces:
    y = surface.getCentroid()[1]
    soil_material_attrs[get_soil_index_from_depth(y)].assignTo(surface)

# Repair anchor line references
for i, attr in enumerate(anchor_line_attrs):
    newlines = [anchor_lines[i][0]] # Add the rod
    for assign in attr.getAssignments():
        line = CastTo(assign.getDatabaseObject(), "IFLine")
        newlines.append(line)
    anchor_lines[i] = newlines # replace with list of all anchor lines

# Delete the temporary attributes
todelete = [retained_surf_attr, anchor_surf_attr, horiz_line_attr] + anchor_line_attrs
for attr in todelete:
    attr.deassignFrom("all")
    database.deleteAttribute(attr)
del retained_surf_attr
del anchor_surf_attr
del horiz_line_attr
del anchor_line_attrs
del todelete

# Generate the mesh
database.resetMesh()
database.updateMesh()

# Deactivate the wall and anchors so we start with just the soil
structure_deactivate_attr.assignTo(wall_lines)
structure_deactivate_attr.assignTo(database.getObjects(anchor_bar_mesh_attr))
structure_deactivate_attr.assignTo(database.getObjects(anchor_grout_mesh_attr))
# Initial stage with gravity
initial_loadcase = Helpers.get_loadcase(1)
initial_loadcase.setName("Initial conditions")
initial_loadcase.addGravity(True)
# The initial loadcase must specify the nonlinear controls. Here we have a basic nonlinear analysis with a manual load increment, i.e 1 increment
initial_loadcase.setTransientControl(0)
initial_loadcase.getTransientControl().setNonlinearManual().setOutput().setConstants()
initial_loadcase.getTransientControl().setValue("dlnorm", 1.0).setValue("dtnrml", 1.0) # Displacment norms
initial_loadcase.getTransientControl().setValue("iterStrategyType", "Minimise including residuals")
# 2nd Stage. Activate the wall elements to represent the installation
install_wall_loadcase = database.createLoadcase("Install wall")
install_wall_loadcase.addGravity(True)
wall_activate_attr.assignTo(wall_lines, lusas.assignment().setAllDefaults().setLoadset(install_wall_loadcase))
# Consider any surcharge loading present before excavation starts
surcharge_loadcase = database.createLoadcase("Surcharge")
surcharge_loadcase.addGravity(True)

# Nonlinear analyses in LUSAS have either manual or automatic incrementation.
# Generally, automatic increments carry forward loading from previous stages, whereas manual do not.
# We'll keep a list of manual loadcases to which loads are assigned as a range once all loadcases are created
manual_loadcases = []
# We also need to apply the dummy load to the excavation loadcases
excavation_loadcases = []

y = soil_depth
prev_i = 0
for i, depth in enumerate(excavation_depths):
    y-=depth
    iy = vertical_coords.index(y)
    print(i, depth, y, iy)
    # Loadcase/stage for the excavation
    lc = database.createLoadcase(f"Excavation {i+1}")
    # Assignment to this loadcase
    assign = lusas.assignment().setAllDefaults().setLoadset(lc)    
    # Deactivate the excavated soil elements in this stage
    excavation_deactivate_attrs[i].assignTo(excavated_surfaces[prev_i:iy], assign)
    # Deactivate the excavated interface elements in this stage
    excavation_deactivate_attrs[i].assignTo(excavated_lines[prev_i:iy], assign)

    # The deactivation will be applied in multiple increments, with a max of 20 increments 
    # starting at 0.1 to load factor of 1
    lc.setTransientControl(20)
    lc.getTransientControl().setNonlinearAutomatic(0.1) # Output and constants will follow initial case
    lc.getTransientControl().setValue("MaxChangeInLoadFactor", 1.0).setValue("MaxLoadFactor", 1.0)
    if i > 0:
        # Assign dummy load
        excavation_loadcases.append(lc)

    # With each excavation (other than the final one) an anchor rod is subsequently installed
    if i < len(anchor_lines):
        # Loadcase/stage for anchor installation
        lc = database.createLoadcase(f"Install Anchor {i+1}")
        # Assignment to this loadcase
        assign = lusas.assignment().setAllDefaults().setLoadset(lc)
        # Activate the anchor elements
        anchor_activation_attrs[i].assignTo(anchor_lines[i], assign)
        # Assign the anchor load to the bar element only
        assign.setTargetStressEnd("start")
        anchor_load_attrs[i].assignTo(anchor_lines[i][0], assign)
        # The anchor load is applied in increments so set the nonlinear automatic control.
        # Note that this will automatically include all previous manual loads
        lc.setTransientControl(20)
        lc.getTransientControl().setNonlinearAutomatic(0.1) # Output and constants will follow initial case
        lc.getTransientControl().setValue("MaxChangeInLoadFactor", 1.0).setValue("MaxLoadFactor", 1.0)

        # Before the next excavation, set the water level to represent the base of the excavation
        lc = database.createLoadcase(f"Set water level for excavation {i+2}")
        lc.addGravity(True)
        # Assignment to this loadcase
        assign = lusas.assignment().setAllDefaults().setLoadset(lc)
        # Assign the water pressure attribute to the bottom of the next excavated surface
        iy2 = vertical_coords.index(y-excavation_depths[i+1])
        water_pressure_attrs[i+1].assignTo(exc_hor_lines[iy2], assign)
        # Assign other loads later
        manual_loadcases.append(lc)

        # Dewatering is achieved by moving the phreatic surface by a prescribed displacement.
        lc = database.createLoadcase(f"Dewatering {i+1}")
        # Assignment to this loadcase
        assign = lusas.assignment().setAllDefaults().setLoadset(lc)
        dewater_load_attrs[i].assignTo(line_water_levels[i+1], assign)
        # Apply draining incrementally
        lc.setTransientControl(20)
        lc.getTransientControl().setNonlinearAutomatic(0.1) # Output and constants will follow initial case
        lc.getTransientControl().setValue("MaxChangeInLoadFactor", 1.0).setValue("MaxLoadFactor", 1.0)
    
    prev_i = iy

# Assign the loading to the manual load steps
# Ground water loads
assign = lusas.assignment().setAllDefaults().setLoadsetSpecified(initial_loadcase)
assign.addLoadsetSpecified(install_wall_loadcase)
assign.addLoadsetSpecified(surcharge_loadcase)
for lc in manual_loadcases:
    assign.addLoadsetSpecified(lc)
water_pressure_attrs[0].assignTo(rhs_lines, assign)

# Surcharge load.
assign = lusas.assignment().setAllDefaults().setLoadsetSpecified(surcharge_loadcase)
for lc in manual_loadcases:
    assign.addLoadsetSpecified(lc)
surchage_load_attr.assignTo(ret_hor_lines[0], assign)

# Dummy load for excavation
if len(excavation_loadcases) > 1:
    assign = lusas.assignment().setAllDefaults().setLoadsetSpecified(excavation_loadcases[0])
    for lc in excavation_loadcases[1:]:
        assign.addLoadsetSpecified(lc)
    dummy_load_attr.assignTo(rhs_lines[0].getStartPoint(), assign)

print("\n" + "="*50)
print("Model building completed successfully!")
print("="*50)
# Users run the model from LUSAS