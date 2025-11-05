# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      502 Tunnel.py
# Author:       Finite Element Analysis Ltd
# Description:  Generates the geometry, assign all attributes, runs LUSAS, and plots the deformed mesh.
#               Users can edit geometry inputs.
#               The MC model is adopted for soil behaviour.
#               joints are not included.
#               Three construction stages are considered: initial, lining installation and tunnel excavation.
#               Inputs data are not checked for validity.
#######################################################################

# Add parent directory to sys.path so that we can load libraries from the parent directory
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(parent_dir)

# Libraries:
from shared.LPI import *
import shared.Helpers as Helpers

# =============================================================================
# MODEL PARAMETERS (all dimensions in metres)
# =============================================================================
radius = 3         # Tunnel radius (m)
b = 20             # Inner box size around tunnel (m)
a = 5              # Refined zone width around inner box (m)
c = 20             # Top extension above tunnel(m)
w = 110            # Total outer width of model(m)
l = 65             # Total outer length (depth) of model(m)
solveModel = True  # Whether to solve the model after creation

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

# Set global analysis parameters
database.setAnalysisCategory("2D Inplane")
database.setVerticalDir("Y")
database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))
Helpers.initialise(lusas)

# Optionally, disable UI
lusas.enableUI(False)

# =============================================================================
# TUNNEL CIRCLE GEOMETRY
# =============================================================================

def create_tunnel_circle(radius : float) -> list['IFPoint']:
    r"""
    Create circular tunnel opening split into four quadrants.
    Args:
        radius (float): tunnel radius in metres
    Returns:
        list[IFPoint]: cardinal points (top, bottom, left, right)
    """
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
    
    points : list['IFPoint'] = database.createPoint(geometry_data).getObjects("Point")
    
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

def identify_quadrants(radius : float) -> dict[str, 'IFLine']:
    r"""
    Identify and return the four quadrant lines of the circle.
    Args:
        radius (float): tunnel radius in metres
    Returns:
        dictionary containing the four quadrant line objects
    """
    lines : list['IFLine'] = database.getObjects("Lines")

    quadrants : dict[str, 'IFLine'] = {}
    
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

def create_base_surface(radius : float, b : float) -> list['IFSurface']:
    r"""
    Create the base surface (top-left quadrant of inner box).
    Args:
        radius (float): tunnel radius
        b (float): inner box size
    Returns:
        list: created surface objects
    """

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

def mirror_surfaces():
    r"""
    Mirror existing surfaces to create right and bottom quadrants.
    This creates all four quadrants around the tunnel from the initial top-left quadrant.
    """
   
    # First mirror horizontally (right), then vertically (bottom)
    for axis in ["right", "bottom"]:

        # Create temporary mirror transformation
        attrTransf = database.createScreenMirrorTransAttr("Trn1")
        attrTransf.setScreenMirror(axis)
        geometry_data = lusas.newGeometryData().setTransformation(attrTransf)

        # Select all existing surfaces in selection
        lusas.selection().remove("all")
        lusas.selection().add(database.getObjects("Surfaces"))

        # Copy-mirror all surfaces
        lusas.selection().add(database.getObjects("Surfaces")).copy(geometry_data)
        
        # Clean up transformation attribute
        database.deleteAttribute(attrTransf)
    
    # Clear selection
    lusas.selection().remove("all")
    
    print(f"Created {database.count('Surfaces')} surfaces")


def create_tunnel_surface(original_quadrants : dict[str, 'IFLine'], cardinal_points : list['IFPoint']) -> tuple['IFSurface', list['IFLine']]:
    r"""
    Create circular tunnel surface from quadrant lines, this creates a separate surface for the tunnel opening.
    Args:
        original_quadrants (dict): original quadrant line objects, cardinal_points (list): cardinal points of the circle
    Returns:
        tuple: (tunnel_surface, copied_lines)
    """

    # Make original geometry unmergeable.
    point_set = lusas.newObjectSet().add(cardinal_points)
    point_set.makeUnmergeable()
    
    line_set = lusas.newObjectSet().add(list(original_quadrants.values()))
    line_set.makeUnmergeable()
    
    # Copy lines in place (zero translation) to create separate tunnel lines
    transform = database.createTranslationTransAttr("Trn2", [0, 0, 0])
    geometry_data = lusas.newGeometryData().setTransformation(transform)

    copied_lines : list['IFLine'] = line_set.copy(geometry_data).keep("Line").getObjects("Line")
    database.deleteAttribute(transform)
    
    # Create circular surface from copied lines
    geometry_data = lusas.newGeometryData().setCreateMethod("coons").setLowerOrderGeometryType("lines")
    tunnel_surface : 'IFSurface' = line_set.createSurface(geometry_data).getObject("Surface")
    
    return tunnel_surface, copied_lines

# =============================================================================
# REFINED MESH ZONES (TRANSITION ZONES AROUND TUNNEL)
# =============================================================================

def create_refined_zones(b: float, a: float, c: float, w: float, l: float) -> dict[str, 'IFSurface']:
    r"""
    Create refined mesh zone surfaces around the tunnel for mesh transition.
    Args:
        b (float): inner box size
        a (float): refined zone width
        c (float): top extension
        w (float): total model width
        l (float): total model depth
    Returns:
        dict: dictionary of all zone surfaces
    """
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

def apply_mesh_attributes(tunnel_surface : 'IFSurface', refined_zones: dict[str, 'IFSurface'], base_surfaces: list['IFSurface']):
    r"""
    Apply mesh attributes to all surfaces with varying element sizes.
        Coarse mesh (1m): Tunnel lining and base surfaces
        Fine mesh (2m): Refined transition zones
        Medium mesh (4m): Outer boundary
    Args:
        tunnel_surface (tunnel opening surface)
        refined_zones (dict): refined zone surfaces
        base_surfaces (list): inner box surfaces
    """
    # ===== GLOBAL SURFACE MESH =====
    print("Applying global surface mesh...")

    # lock the mesh for faster processing
    lusas.database().setMeshLock(True)

    surf_mesh = database.createMeshSurface("Shell Mesh")
    surf_mesh.setRegular("QPN8", 0, 0, True)  # 8-node quadrilateral elements
    surf_mesh.assignTo(database.getObjects("Surfaces"), 1)
    
    # ===== FINE MESH FOR REFINED ZONES =====
    print("Applying fine mesh (2m) to refined zones...")
    fine_mesh = database.createMeshLine("EL 2").setSize("NULL", 2)
    
    for name, surface in refined_zones.items():
        if name != 'outer':  # Skip outer zone (different mesh size)
            lines = lusas.newObjectSet().add(surface).addLOF("Lines").getObjects("Line")
            fine_mesh.assignTo(lines)
    
    # ===== MEDIUM MESH FOR OUTER BOUNDARY =====
    outerLines : list['IFLine'] = lusas.newObjectSet().add(refined_zones['outer']).addLOF("Lines").getObjects("Line")
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
            mesh_Outerzonelines.assignTo(line)
    
    # ===== COARSE MESH FOR TUNNEL AND BASE SURFACES =====
    print("Applying coarse mesh (1m) to tunnel and base surfaces...")
    coarse_mesh = database.createMeshLine("EL 1").setSize("NULL", 1)
    
    # Tunnel surface lines
    tunnel_lines = lusas.newObjectSet().add(tunnel_surface).addLOF("Lines").getObjects("Line")
    coarse_mesh.assignTo(tunnel_lines)
    
    # Base surface lines
    for surf in base_surfaces:
        surf_lines = lusas.newObjectSet().add(surf).addLOF("Lines").getObjects("Line")
        coarse_mesh.assignTo(surf_lines)

    # Unlock the mesh after processing (will also update the mesh)
    lusas.database().setMeshLock(False)

# =============================================================================
# SOIL-STRUCTURE INTERFACE (JOINT ELEMENTS)
# =============================================================================

def create_interface_joints(tunnel_lines : list['IFLine'], original_quadrants : dict[str, 'IFLine']):
    r"""
    Create joint elements at soil-structure interface.
    Args:
        tunnel_lines (list): Lines defining tunnel lining
        original_quadrants (dict): original quadrant lines for interface
    """
    
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
    geomAttr.assignTo(tunnel_lines)

# =============================================================================
# MATERIALS (SOIL AND CONCRETE)
# =============================================================================

def create_soil_material():
    r"""
    Create and assign soil material properties using Modified Mohr-Coulomb plasticity model.
    """
    
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
    soil_material.assignTo(surfaces)


def create_concrete_material(tunnel_lines : list['IFLine']):
    r"""
    Create and assign concrete material properties for tunnel lining.
    Args:
        tunnel_lines (list): Lines defining tunnel lining
    """
    
    print("Creating concrete material...")
    
    # Lining mesh (beam elements)
    wall_mesh = database.createMeshLine("Lining").setSize("BMI3N", 1)  # 3-node beam
    wall_mesh.assignTo(tunnel_lines)
    
    # Concrete material properties
    concrete_material = database.createIsotropicMaterial("Concrete", 14.0e6, 0.2, 2.4)  # E=14GPa, nu=0.2, rho=2.4t/m³
    concrete_material.setValue("alpha", 10.0e-6)  # Thermal expansion coefficient
    concrete_material.assignTo(tunnel_lines)


# =============================================================================
# BOUNDARY CONDITIONS (SUPPORTS)
# =============================================================================
def apply_supports(refined_zones : dict[str, 'IFSurface'], w : float, l : float, c : float, b : float):
    
    print("Creating support attributes...")
    
    # ===== FIXED XY SUPPORT (BOTTOM BOUNDARY) =====
    fix_xy_support_attr = database.createSupportStructural("FixXY")
    fix_xy_support_attr.setStructural("R", "R", "F", "F", "F", "F", "F", "F", "C", "F")
    
    # ===== FIXED X SUPPORT (SIDE BOUNDARIES) =====
    fix_x_support_attr = database.createSupportStructural("FixX")
    fix_x_support_attr.setStructural("R", "F", "F", "F", "F", "F", "F", "F", "C", "F")
    
    # ===== GET OUTER BOUNDARY LINES =====
    outerLines : list['IFLine'] = lusas.newObjectSet().add(refined_zones['outer']).addLOF("Lines").getObjects("Line")
    
    # ===== APPLY SUPPORTS BASED ON LINE POSITION =====
    for line in outerLines:
        start_x = line.getStartPoint().getX()
        start_y = line.getStartPoint().getY()
        end_x = line.getEndPoint().getX()
        end_y = line.getEndPoint().getY()
        
        # Bottom boundary (Y = -l + c + b/2)
        if start_y == -l + c + b/2 and end_y == -l + c + b/2:
            fix_xy_support_attr.assignTo(line)
        
        # Left boundary (X = -w/2)
        elif start_x == -w/2 and end_x == -w/2:
            fix_x_support_attr.assignTo(line)
        
        # Right boundary (X = w/2)
        elif start_x == w/2 and end_x == w/2:
            fix_x_support_attr.assignTo(line)


# =============================================================================
# MAIN EXECUTION SEQUENCE
# =============================================================================

print("\n" + "="*70)
print("STEP 1: Creating tunnel circle geometry")
cardinal_points = create_tunnel_circle(radius)
quadrants = identify_quadrants(radius)

print("\n" + "="*70)
print("STEP 2: Creating base surfaces and mirroring")
base_surface = create_base_surface(radius, b)
mirror_surfaces()

print("\n" + "="*70)
print("STEP 3: Creating tunnel surface")
tunnel_surface, lining_lines = create_tunnel_surface(quadrants, cardinal_points)

print("\n" + "="*70)
print("STEP 4: Creating refined mesh zones")
refined_zones = create_refined_zones(b, a, c, w, l)

print("\n" + "="*70)
print("STEP 5: Applying mesh attributes")
base_surfaces : list['IFSurface'] = database.getObjects("Surfaces")[:4]
apply_mesh_attributes(tunnel_surface, refined_zones, base_surfaces)

print("\n" + "="*70)
print("STEP 6: Creating interface joints")
create_interface_joints(lining_lines, quadrants)

print("\n" + "="*70)
print("STEP 7: Creating and assigning materials")
create_soil_material()
create_concrete_material(lining_lines)

print("\n" + "="*70)
print("STEP 8: Applying boundary conditions")
apply_supports(refined_zones, w, l, c, b)


# =============================================================================
# LOADCASE SETUP (EXCAVATION SEQUENCE)
# =============================================================================

print("\n" + "="*70)
print("LOADCASE SETUP: Configuring excavation sequence")

# ===== LOADCASE 1: INITIAL STATE =====
print("\nConfiguring Loadcase 1: Initial ground state...")
# Get initial loadcase
initial_loadcase : 'IFLoadcase' = database.getLoadset("Loadcase 1", 0)
# Add gravity
initial_loadcase.addGravity(True)
initial_loadcase.setGravityFactor(1.0)
# Add nonlinear and transient control
initial_loadcase.setTransientControl(0)
initial_loadcase.getTransientControl().setNonlinearManual().setOutput().setConstants()
initial_loadcase.getTransientControl().setValue("dlnorm", 0.1).setValue("dtnrml", 0.1)  # Displacement norms

# Deactivate lining and joints
attrDeact = database.createDeactivate("Deact1")
attrDeact.setDeactivate("activeMesh", 100.0, 1.0E-6)
# Assign lining and joints
assignment = lusas.newAssignment().setLoadset("Loadcase 1")
attrDeact.assignTo(lining_lines, assignment)
attrDeact.assignTo(list(quadrants.values()), assignment)

# ===== LOADCASE 2: LINING ACTIVATION =====
print("Configuring Loadcase 2: Lining installation...")
loadcase2 = database.createLoadcase("Loadcase 2", "Analysis 1", 0, False)
# Add gravity
loadcase2.addGravity(True)
loadcase2.setGravityFactor(1.0)
# Position after initial loadcase
loadcase2.moveAfter(initial_loadcase, True)
# Add nonlinear and transient control
loadcase2.setTransientControl(0)
loadcase2.getTransientControl().setNonlinearManual()

# Activate lining and joints (tunnel construction)
attr = database.createActivate("Act1")
assignment = lusas.newAssignment().setLoadset("Loadcase 2")
attr.assignTo(lining_lines, assignment)
attr.assignTo(list(quadrants.values()), assignment)

# ===== LOADCASE 3: TUNNEL EXCAVATION =====
print("Configuring Loadcase 3: Tunnel excavation...")
loadcase3 = database.createLoadcase("Loadcase 3", "Analysis 1", 0, False)
# Add gravity
loadcase3.addGravity(True)
loadcase3.setGravityFactor(1.0)
# Position after lining installation loadcase
loadcase3.moveAfter(loadcase2, True)
# Add nonlinear and transient control
loadcase3.setTransientControl(0)
loadcase3.getTransientControl().setNonlinearManual()

# Deactivate tunnel interior (material removal)
assignment = lusas.newAssignment().setLoadset("Loadcase 3")
attrDeact.assignTo(tunnel_surface, assignment)

# Ensure the UI gets enabled
lusas.enableUI(True)

# =============================================================================
# SAVE AND ANALYZE
# =============================================================================

print("\n" + "="*70)
print("FINALIZING MODEL")

# Save the model
print("Saving model...")
lusas.getProject().save()

# Start analysis
if(solveModel):
    print("Starting analysis...")
    database.getAnalysis("Analysis 1").solve(False)
    database.openAllResults(False)

# Set last loadcase as active
lusas.view().setActiveLoadset(loadcase3)

print("\n" + "="*70)
print("MODEL CREATION COMPLETE!")
print("\nTunnel model successfully created and analysis started.")
print("Check LUSAS interface for analysis progress.")
print("\nExcavation sequence:")
print("  - Loadcase 1: Initial ground state (lining deactivated)")
print("  - Loadcase 2: Lining installation (lining activated)")
print("  - Loadcase 3: Tunnel excavation (interior material removed)")