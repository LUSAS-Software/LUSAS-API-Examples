# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      502 Tunnel.py
# Author:       Finite Element Analysis Ltd
# Description:  Generates the geometry, assign all attributes, runs LUSAS, and plots the deformed mesh.
#               Users can edit geometry inputs.
#               The MC model is adopted for soil behaviour.
#               joints are not included.
#               Three construction stages are considered: initial, linign installation and tunnel excavation.
#               Inputs data are not checked for validity.
#######################################################################

import os
from shared.LPI import *
import shared.Helpers as Helpers
import time

# Clear console for clean output
os.system('cls' if os.name == 'nt' else 'clear')

# =============================================================================
# MODEL PARAMETERS (all dimensions in metres)
# =============================================================================
radius = 3      # Tunnel radius (m)
b = 20          # Inner box size around tunnel (m)
a = 5           # Refined zone width around inner box (m)
c = 20          # Top extension above tunnel(m)
w = 110         # Total outer width of model(m)
l = 65          # Total outer length (depth) of model(m)

print("Starting tunnel model creation...")

# =============================================================================
# INITIALIZE MODEL
# =============================================================================
# Get LUSAS modeller instance
lusas = get_lusas_modeller()

# Safety check: prevent overwriting unsaved work
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("Please save or close the current model before running.")

# Create new project and get database reference
lusas.newProject("Structural", "Tunnel.mdl")
database = lusas.getDatabase()
lusas.setVisible(True)
lusas.enableUI(True)

# Set global analysis parameters
database.setAnalysisCategory("2D Inplane")
database.setVerticalDir("Y")
database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))
Helpers.initialise(lusas)

# =============================================================================
# TUNNEL CIRCLE GEOMETRY
# =============================================================================

# Create circular tunnel opening split into four quadrants.
# Args: radius (float): tunnel radius in metres
# Returns:list: cardinal points (top, bottom, left, right)
def create_tunnel_circle(radius):
    # Create four cardinal points on the circle
    geometry_data = lusas.geometryData().setAllDefaults()
    geometry_data.setLowerOrderGeometryType("coordinates")
    
    coords = [
        (0, radius, 0),      # Top point
        (0, -radius, 0),     # Bottom point
        (radius, 0, 0),      # Right point
        (-radius, 0, 0)      # Left point
    ]
    
    for x, y, z in coords:
        geometry_data.addCoords(x, y, z)
    
    points = database.createPoint(geometry_data).getObjects("Point")
    
    # Create full circle using three points (top-bottom-right defines circle)
    geometry_data = lusas.geometryData().setAllDefaults()
    geometry_data.setLowerOrderGeometryType("coordinates")
    geometry_data.makeCircle()
    geometry_data.setStartMiddleEnd()
    
    for x, y, z in [(0, radius, 0), (0, -radius, 0), (radius, 0, 0)]:
        geometry_data.addCoords(x, y, z)
    
    database.createLine(geometry_data)
    
    # Split the complete circle into four quadrants at cardinal points
    lusas.selection().remove("all")
    lusas.selection().add(database.getObjects("Line"))
    lusas.selection().add(database.getObjects("Point"))
    lusas.selection().splitLine()
    
    return points

# Identify and return the four quadrant lines of the circle.
# Args: radius (float), tunnel radius in metres
# Returns: dictionary containing the four quadrant line objects

def identify_quadrants(radius):
    
    lines = database.getObjects("Lines")
    quadrants = {
        "left_top": None, 
        "right_top": None, 
        "left_bottom": None, 
        "right_bottom": None
    }
    
    # Classify each line by checking endpoint positions
    for ln in lines:
        sx, sy = ln.getStartPoint().getX(), ln.getStartPoint().getY()
        ex, ey = ln.getEndPoint().getX(), ln.getEndPoint().getY()
        
        is_top = (sy == radius or ey == radius)
        is_left = (sx == -radius or ex == -radius)
        
        if is_top:
            quadrants["left_top" if is_left else "right_top"] = ln
        else:
            quadrants["left_bottom" if is_left else "right_bottom"] = ln
    
    return quadrants


# =============================================================================
# BASE SURFACES (INNER BOX AROUND TUNNEL)
# =============================================================================

# Create the base surface (top-left quadrant of inner box).
# Args:radius (float): tunnel radius, b (float): inner box size
# Returns: list: created surface objects
def create_base_surface(radius, b):

    # Define five boundary lines for the top-left quadrant
    lines = [
        Helpers.create_line_by_coordinates(0, radius, 0, 0, b/2, 0),          # Top of circle to top center
        Helpers.create_line_by_coordinates(0, b/2, 0, -b/2, b/2, 0),          # Top center to top-left corner
        Helpers.create_line_by_coordinates(-b/2, b/2, 0, -b/2, 0, 0),         # Top-left to middle-left
        Helpers.create_line_by_coordinates(-b/2, 0, 0, -radius, 0, 0),        # Middle-left to left of circle
        quadrants["left_top"]                                                  # Left quadrant of circle
    ]
    
    # Create surface
    geometry_data = lusas.geometryData().setAllDefaults()
    geometry_data.setCreateMethod("coons")
    geometry_data.setLowerOrderGeometryType("lines")
    
    line_set = lusas.newObjectSet()
    line_set.add(lines)
    return line_set.createSurface(geometry_data).getObjects("Surface")

# Mirror existing surfaces to create right and bottom quadrants.
# This creates all four quadrants around the tunnel from the initial top-left quadrant.
def mirror_surfaces():
   
    # First mirror horizontally (right), then vertically (bottom)
    for axis in ["right", "bottom"]:
        for surface in database.getObjects("Surfaces"):
            lusas.selection().remove("All")
            lusas.selection().add(surface)
            
            # Create temporary mirror transformation
            attr = database.createScreenMirrorTransAttr("Trn1")
            attr.setScreenMirror(axis)
            transform = database.getTransformation("Trn1")
            
            # Copy surface with mirror transformation
            geometry_data = lusas.geometryData().setAllDefaults()
            geometry_data.setTransformation(transform)
            lusas.selection().copy(geometry_data)
            database.updateMesh()
            
            # Clean up transformation attribute
            del attr, transform
    
    lusas.selection().remove("all")
    print(f"Created {database.count('Surfaces')} surfaces")

# Create circular tunnel surface from quadrant lines, this creates a separate surface for the tunnel opening.
# Args: original_quadrants (dict): original quadrant line objects, cardinal_points (list): cardinal points of the circle
# Returns:tuple: (tunnel_surface, copied_lines)
def create_tunnel_surface(original_quadrants, cardinal_points):
   
    # Make original geometry unmergeable.
    point_set = lusas.newObjectSet()
    point_set.add(cardinal_points)
    point_set.makeUnmergeable()
    
    line_set = lusas.newObjectSet()
    line_set.add(list(original_quadrants.values()))
    line_set.makeUnmergeable()
    
    # Copy lines in place (zero translation) to create separate tunnel lines
    transform = database.createTranslationTransAttr("Trn2", [0, 0, 0])
    geometry_data = lusas.newGeometryData()
    geometry_data.setAllDefaults()
    geometry_data.setTransformation(transform)
    
    copied_lines = line_set.copy(geometry_data).keep("Line").getObjects("Line")
    database.deleteAttribute(transform)
    
    # Create circular surface from copied lines
    geometry_data = lusas.geometryData().setAllDefaults()
    geometry_data.setCreateMethod("coons")
    geometry_data.setLowerOrderGeometryType("lines")
    
    copied_line_set = lusas.newObjectSet()
    copied_line_set.add(line_set)
    tunnel_surface = copied_line_set.createSurface(geometry_data).getObject("Surface")
    
    return tunnel_surface, copied_lines

# =============================================================================
# REFINED MESH ZONES (TRANSITION ZONES AROUND TUNNEL)
# =============================================================================

# Create all refined mesh zone surfaces around the tunnel. These zones provide mesh transition from fine (near tunnel) to coarse (far field).
# Args: b (float): inner box size, a (float): refined zone width, c (float): top extension, w (float): total model width, l (float): total model depth
# Returns: dict: dictionary of all zone surfaces
def create_refined_zones(b, a, c, w, l):
    
    zones = {}
    
    # ===== TOP ROW (above tunnel) =====
    zones['top_left'] = Helpers.create_surface_by_coordinates(
        [-b/2, -b/2, -b/2-a, -b/2-a], 
        [b/2, b/2+c, b/2+c, b/2], 
        [0, 0, 0, 0]
    )
    
    zones['top_center'] = Helpers.create_surface_by_coordinates(
        [-b/2, -b/2, b/2, b/2, 0], 
        [b/2, b/2+c, b/2+c, b/2, b/2], 
        [0, 0, 0, 0, 0]
    )
    
    zones['top_right'] = Helpers.create_surface_by_coordinates(
        [b/2, b/2, b/2+a, b/2+a], 
        [b/2, b/2+c, b/2+c, b/2], 
        [0, 0, 0, 0]
    )
    
    # ===== MIDDLE ROW (sides of tunnel) =====
    zones['left'] = Helpers.create_surface_by_coordinates(
        [-b/2, -b/2, -b/2-a, -b/2-a, -b/2], 
        [0, b/2, b/2, -b/2, -b/2], 
        [0, 0, 0, 0, 0]
    )
    
    zones['right'] = Helpers.create_surface_by_coordinates(
        [b/2, b/2, b/2+a, b/2+a, b/2], 
        [0, b/2, b/2, -b/2, -b/2], 
        [0, 0, 0, 0, 0]
    )
    
    # ===== BOTTOM ROW (below tunnel) =====
    zones['bottom_left'] = Helpers.create_surface_by_coordinates(
        [-b/2, -b/2-a, -b/2-a, -b/2], 
        [-b/2, -b/2, -b/2-a, -b/2-a], 
        [0, 0, 0, 0]
    )
    
    zones['bottom_center'] = Helpers.create_surface_by_coordinates(
        [0, -b/2, -b/2, b/2, b/2], 
        [-b/2, -b/2, -b/2-a, -b/2-a, -b/2], 
        [0, 0, 0, 0, 0]
    )
    
    zones['bottom_right'] = Helpers.create_surface_by_coordinates(
        [b/2, b/2+a, b/2+a, b/2], 
        [-b/2, -b/2, -b/2-a, -b/2-a], 
        [0, 0, 0, 0]
    )
    
    # ===== OUTER BOUNDARY (far field) =====
    zones['outer'] = Helpers.create_surface_by_coordinates(
        [-b/2-a, -w/2, -w/2, w/2, w/2, b/2+a, 
         b/2+a, b/2+a, b/2+a, b/2, -b/2, -b/2-a, -b/2-a, -b/2-a],
        [b/2+c, b/2+c, -l+b/2+c, -l+b/2+c, b/2+c, b/2+c, 
         b/2, -b/2, -b/2-a, -b/2-a, -b/2-a, -b/2-a, -b/2, b/2],
        [0] * 14
    )
    
    return zones

# =============================================================================
# MESH ATTRIBUTES (DEFINE ELEMENT SIZES)
# =============================================================================

# Apply mesh attributes to all surfaces with varying element sizes.
    # Coarse mesh (1m): Tunnel lining and base surfaces
    # Fine mesh (2m): Refined transition zones
    # Medium mesh (4m): Outer boundary
    
# Args:tunnel_surface (tunnel opening surface), refined_zones (dict): refined zone surfaces, base_surfaces (list): inner box surfaces
def apply_mesh_attributes(tunnel_surface, refined_zones, base_surfaces):

    # ===== GLOBAL SURFACE MESH =====
    print("Applying global surface mesh...")
    surf_mesh = database.createMeshSurface("Shell Mesh")
    surf_mesh.setRegular("QPN8", 0, 0, True)  # 8-node quadrilateral elements
    surf_mesh.assignTo(database.getObjects("Surfaces"), 1)
    database.updateMesh()
    
    # ===== FINE MESH FOR REFINED ZONES =====
    print("Applying fine mesh (2m) to refined zones...")
    fine_mesh = database.createMeshLine("EL 2").setSize("NULL", 2)
    
    for name, surface in refined_zones.items():
        if name != 'outer':  # Skip outer zone (different mesh size)
            lines = lusas.newObjectSet().add(surface).addLOF("Lines").getObjects("Line")
            fine_mesh.assignTo(lines, 1)
    
    # ===== MEDIUM MESH FOR OUTER BOUNDARY =====
    outerLines = lusas.newObjectSet().add(refined_zones['outer']).addLOF("Lines").getObjects("Line")
    mesh_Outerzonelines = database.createMeshLine("EL 4").setSize("NULL", 4)
    
    for line in outerLines:
        start_x = line.getStartPoint().getX()
        start_y = line.getStartPoint().getY()
        end_x = line.getEndPoint().getX()
        end_y = line.getEndPoint().getY()
        
        # Check line position to assign mesh
        if (start_y == -l + c + b/2 and end_y == -l + c + b/2) or \
           (start_x == -w/2 and end_x == -w/2) or \
           (start_x == w/2 and end_x == w/2) or \
           (start_y == b/2+c and end_y == b/2+c):
            mesh_Outerzonelines.assignTo(line, 1)
    
    # ===== COARSE MESH FOR TUNNEL AND BASE SURFACES =====
    print("Applying coarse mesh (1m) to tunnel and base surfaces...")
    coarse_mesh = database.createMeshLine("EL 1").setSize("NULL", 1)
    
    # Tunnel surface lines
    tunnel_lines = lusas.newObjectSet().add(tunnel_surface).addLOF("Lines").getObjects("Line")
    coarse_mesh.assignTo(tunnel_lines, 1)
    
    # Base surface lines
    for surf in base_surfaces:
        surf_lines = lusas.newObjectSet().add(surf).addLOF("Lines").getObjects("Line")
        coarse_mesh.assignTo(surf_lines, 1)
    
    database.updateMesh()


# =============================================================================
# SOIL-STRUCTURE INTERFACE (JOINT ELEMENTS)
# =============================================================================

# Create joint elements at soil-structure interface.
# Args: tunnel_lines: Lines defining tunnel lining, original_quadrants (dict): original quadrant lines for interface
def create_interface_joints(tunnel_lines, original_quadrants):
    
    # ===== CREATE JOINT MESH ATTRIBUTE =====
    joint_mesh = database.createMeshLine("Joint").setSize("JNT3", 1)
    
    # ===== CREATE JOINT MATERIAL (STIFF SPRINGS) =====
    joint_material = database.createSpringJointMaterial("soil-stru joint", [1e6, 1e6])
    joint_material.setValue("Assignment", "Line")
    
    # ===== SELECT TUNNEL SURFACE LINES =====
    selected_lines = lusas.getSelection().add(tunnel_lines)
    memory = lusas.getSelectionMemory().add(selected_lines)
    lusas.getSelection().remove("All")
    
    # ===== SELECT ORIGINAL QUADRANT LINES =====
    quadrant_lines = list(original_quadrants.values())
    for line in quadrant_lines:
        lusas.getSelection().add(line)
    
    # ===== ASSIGN JOINT MESH =====
    assignment = lusas.assignment().setAllDefaults()
    database.getAttribute("Line Mesh", "Joint").assignTo(quadrant_lines, memory, assignment)
    
    # ===== ASSIGN JOINT MATERIAL =====
    lusas.getSelectionMemory().remove("All")
    lusas.getSelection().remove("All")
    selected_lines = lusas.getSelection().add(quadrant_lines)
    assignment = lusas.assignment().setAllDefaults()
    assignment.setLoadset("Loadcase 1")
    database.getAttribute("Joint Material", "soil-stru joint").assignTo(selected_lines, assignment)
    
    lusas.getSelection().remove("All")
    database.updateMesh()
    print("Soil-structure interface joints created")
    
    # ===== CREATE GEOMETRIC ATTRIBUTE FOR LINING =====
    print("Creating geometric attributes...")
    geomAttr = database.createGeometricLine("Lining")
    geomAttr.setPlaneStrain("0.4")  # Thickness = 0.4m
    geomAttr.setAnalysisCategory("2D Inplane")
    geomAttr.assignTo(tunnel_lines, 1)

# =============================================================================
# MATERIALS (SOIL AND CONCRETE)
# =============================================================================

# Create and assign soil material properties, Modified Mohr-Coulomb plasticity model.
def create_soil_material():
    
    print("Creating soil material...")
    
    # Elastic properties
    soil_material = database.createIsotropicMaterial("Soil", 35e3, 0.3, 2)  # E=35MPa, nu=0.3, rho=2t/m³
    soil_material.setValue("alpha", 0.000012)  # Thermal expansion coefficient
    
    # Plastic properties (Modified Mohr-Coulomb)
    soil_material.addPlasticModifiedMohrCoulomb("No", 38, 8, 0, 0)  # phi=38°, psi=8°
    soil_material.addModifiedMohrCoulombCohesion(0, 10)  # Cohesion = 10 kPa
    soil_material.addKoElasticRow(0.0, 0.384)  # Ko = 0.384
    
    # Assign to all surfaces
    surfaces = database.getObjects("Surfaces")
    soil_material.assignTo(surfaces, 1)


# Create and assign concrete material for tunnel lining.
# Args:tunnel_lines: lines defining tunnel lining
def create_concrete_material(tunnel_lines):
    
    print("Creating concrete material...")
    
    # Lining mesh (beam elements)
    wall_mesh = database.createMeshLine("Lining").setSize("BMI3N", 1)  # 3-node beam
    wall_mesh.assignTo(tunnel_lines, 1)
    
    # Concrete material properties
    concrete_material = database.createIsotropicMaterial("Concrete", 14.0e6, 0.2, 2.4)  # E=14GPa, nu=0.2, rho=2.4t/m³
    concrete_material.setValue("alpha", 10.0e-6)  # Thermal expansion coefficient
    concrete_material.assignTo(tunnel_lines, 1)


# =============================================================================
# BOUNDARY CONDITIONS (SUPPORTS)
# =============================================================================
def apply_supports(refined_zones, w, l, c, b):
    
    print("Creating support attributes...")
    
    # ===== FIXED XY SUPPORT (BOTTOM BOUNDARY) =====
    fix_xy_support_attr = database.createSupportStructural("FixXY")
    fix_xy_support_attr.setStructural("R", "R", "F", "F", "F", "F", "F", "F", "C", "F")
    
    # ===== FIXED X SUPPORT (SIDE BOUNDARIES) =====
    fix_x_support_attr = database.createSupportStructural("FixX")
    fix_x_support_attr.setStructural("R", "F", "F", "F", "F", "F", "F", "F", "C", "F")
    
    # ===== GET OUTER BOUNDARY LINES =====
    outerLines = lusas.newObjectSet().add(refined_zones['outer']).addLOF("Lines").getObjects("Line")
    
    # ===== APPLY SUPPORTS BASED ON LINE POSITION =====
    for line in outerLines:
        start_x = line.getStartPoint().getX()
        start_y = line.getStartPoint().getY()
        end_x = line.getEndPoint().getX()
        end_y = line.getEndPoint().getY()
        
        # Bottom boundary (Y = -l + c + b/2)
        if start_y == -l + c + b/2 and end_y == -l + c + b/2:
            fix_xy_support_attr.assignTo(line, 1)
        
        # Left boundary (X = -w/2)
        elif start_x == -w/2 and end_x == -w/2:
            fix_x_support_attr.assignTo(line, 1)
        
        # Right boundary (X = w/2)
        elif start_x == w/2 and end_x == w/2:
            fix_x_support_attr.assignTo(line, 1)


# =============================================================================
# MAIN EXECUTION SEQUENCE
# =============================================================================

print("\n" + "="*70)
print("STEP 1: Creating tunnel circle geometry")
print("="*70)
cardinal_points = create_tunnel_circle(radius)
quadrants = identify_quadrants(radius)

print("\n" + "="*70)
print("STEP 2: Creating base surfaces and mirroring")
print("="*70)
base_surface = create_base_surface(radius, b)
mirror_surfaces()

print("\n" + "="*70)
print("STEP 3: Creating tunnel surface")
print("="*70)
tunnel_surface, lining_lines = create_tunnel_surface(quadrants, cardinal_points)

print("\n" + "="*70)
print("STEP 4: Creating refined mesh zones")
print("="*70)
refined_zones = create_refined_zones(b, a, c, w, l)

print("\n" + "="*70)
print("STEP 5: Applying mesh attributes")
print("="*70)
base_surfaces = database.getObjects("Surfaces")[:4]
apply_mesh_attributes(tunnel_surface, refined_zones, base_surfaces)

print("\n" + "="*70)
print("STEP 6: Creating interface joints")
print("="*70)
create_interface_joints(lining_lines, quadrants)

print("\n" + "="*70)
print("STEP 7: Creating and assigning materials")
print("="*70)
create_soil_material()
create_concrete_material(lining_lines)

print("\n" + "="*70)
print("STEP 8: Applying boundary conditions")
print("="*70)
apply_supports(refined_zones, w, l, c, b)


# =============================================================================
# LOADCASE SETUP (EXCAVATION SEQUENCE)
# =============================================================================

print("\n" + "="*70)
print("LOADCASE SETUP: Configuring excavation sequence")
print("="*70)

# ===== LOADCASE 1: INITIAL STATE =====
print("\nConfiguring Loadcase 1: Initial ground state...")
initial_loadcase = database.getLoadset("Loadcase 1", 0)
initial_loadcase.addGravity(True)
initial_loadcase.setGravityFactor(1.0)
initial_loadcase.setTransientControl(0)
initial_loadcase.getTransientControl().setNonlinearManual().setOutput().setConstants()
initial_loadcase.getTransientControl().setValue("dlnorm", 0.1).setValue("dtnrml", 0.1)  # Displacement norms

# Deactivate lining and joints
attr = database.createDeactivate("Deact1")
attr.setDeactivate("activeMesh", 100.0, 1.0E-6)
assignment = lusas.assignment().setAllDefaults()
assignment = lusas.assignment().setLoadset("Loadcase 1")
database.getAttribute("Deactivate", "Deact1").assignTo(lining_lines, assignment)
database.getAttribute("Deactivate", "Deact1").assignTo(list(quadrants.values()), assignment)

# ===== LOADCASE 2: LINING ACTIVATION =====
print("Configuring Loadcase 2: Lining installation...")
loadcase2 = database.createLoadcase("Loadcase 2", "Analysis 1", 0, False)
loadcase2.addGravity(True)
loadcase2.setGravityFactor(1.0)
target = database.getLoadset("Loadcase 1", 0)
loadcase2.moveAfter(target, True)
lusas.getCurrentView().setActiveLoadset(loadcase2)

loadcase2.setTransientControl(0)
loadcase2.getTransientControl().setValue("CouplingReadInterval", 1.0).setValue("CouplingWriteInterval", 1.0)
loadcase2.getTransientControl().setNonlinearManual()

# Activate lining and joints (tunnel construction)
attr = database.createActivate("Act1")
assignment = lusas.assignment().setAllDefaults()
assignment = lusas.assignment().setLoadset("Loadcase 2")
database.getAttribute("Activate", "Act1").assignTo(lining_lines, assignment)
database.getAttribute("Activate", "Act1").assignTo(list(quadrants.values()), assignment)

# ===== LOADCASE 3: TUNNEL EXCAVATION =====
print("Configuring Loadcase 3: Tunnel excavation...")
loadcase3 = database.createLoadcase("Loadcase 3", "Analysis 1", 0, False)
loadcase3.addGravity(True)
loadcase3.setGravityFactor(1.0)
target = database.getLoadset("Loadcase 2", 0)
loadcase3.moveAfter(target, True)
lusas.getCurrentView().setActiveLoadset(loadcase3)

# Deactivate tunnel interior (material removal)
attr = database.createDeactivate("Deact2")
attr.setDeactivate("activeMesh", 100.0, 1.0E-6)
assignment = lusas.assignment().setAllDefaults()
assignment = lusas.assignment().setLoadset("Loadcase 3")
database.getAttribute("Deactivate", "Deact2").assignTo(tunnel_surface, assignment)

loadcase3.setTransientControl(0)
loadcase3.getTransientControl().setValue("CouplingReadInterval", 1.0).setValue("CouplingWriteInterval", 1.0)
loadcase3.getTransientControl().setNonlinearManual()


# =============================================================================
# SAVE AND ANALYZE
# =============================================================================

print("\n" + "="*70)
print("FINALIZING MODEL")
print("="*70)

# Save the model
print("\nSaving model...")
lusas.getProject().save()

# Start analysis
print("\nStarting analysis...")
database.getAnalysis("Analysis 1").solve(False)
database.openAllResults(False)

print("\n" + "="*70)
print("MODEL CREATION COMPLETE!")
print("="*70)
print("\nTunnel model successfully created and analysis started.")
print("Check LUSAS interface for analysis progress.")
print("\nExcavation sequence:")
print("  - Loadcase 1: Initial ground state (lining deactivated)")
print("  - Loadcase 2: Lining installation (lining activated)")
print("  - Loadcase 3: Tunnel excavation (interior material removed)")
print("="*70)