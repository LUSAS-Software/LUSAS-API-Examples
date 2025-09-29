# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      501 Bridge abutment.py
# Author:       Finite Element Analysis Ltd
# Description:  Generates the geometry, assign all attributes, runs LUSAS, and plots the deformed mesh.
#               Users can edit geometry inputs.
#               The MC model is adopted for soil behaviour.
#               Interfaces and joints are not included.
#######################################################################

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

#######################################################################
# DIMENSION INPUTS - Edit these values directly in the editor
#######################################################################

# Dimensions in meters (adjust these values as needed)

d = 12.0    # Distance of abutment from right side, 3-100
t = 3.0     # Distance of slope toe from left side,1-100
s = 5.0     # Distance of the abutment from slope crest,1-10
w = 30.0    # Model width, should not be less than d+t+s+2, d+t+s+2,100
h3 = 5      # upper part model height 2,100
h4 = 3.5    # free part of the abutement length (less than h3-2), 1:h3-1
h1 = 8.0    # Model left side depth, 1:h2
h2 = 11.5   # Model Right side depth (not less than h1+2),h1:100
f = 5.0     # distributed load projecion (less than d-2), minimum 1m
b = 1.5     # Half-width of the abutment base 1-2m

#######################################################################
# PARAMETER VALIDATION
#######################################################################

print("Bridge Abutment Model Creator")
print("=" * 60)
print("Current dimensions:")
print(f"d = {d}m (Distance of abutment from right side)")
print(f"t = {t}m (Distance of slope toe from left side)")
print(f"s = {s}m (Distance of abutment from slope crest)")
print(f"w = {w}m (Model width)")
print(f"h1 = {h1}m (Model left side depth)")
print(f"h2 = {h2}m (Model right side depth)")
print(f"h3 = {h3}m (Upper part model height)")
print(f"h4 = {h4}m (Free part of abutment length)")
print(f"f = {f}m (Distributed load projection)")
print(f"b = {b}m (Half-width of abutment base)")
print("=" * 60)

# Validate all input parameters according to the specified constraints
print("Validating parameters...")
errors = []

# Validate d (Distance of abutment from right side: 3-100)
if not (3 <= d <= 100):
    errors.append(f"Parameter 'd' = {d} must be between 3 and 100 meters")

# Validate t (Distance of slope toe from left side: 1-100)
if not (1 <= t <= 100):
    errors.append(f"Parameter 't' = {t} must be between 1 and 100 meters")

# Validate s (Distance of abutment from slope crest: 1-10)
if not (1 <= s <= 10):
    errors.append(f"Parameter 's' = {s} must be between 1 and 10 meters")

# Validate w (Model width: should not be less than d+t+s+2, range: d+t+s+2 to 100)
min_w = d + t + s + 2
if w < min_w:
    errors.append(f"Parameter 'w' = {w} must not be less than d+t+s+2 = {min_w}")
if w > 100:
    errors.append(f"Parameter 'w' = {w} must not exceed 100 meters")

# Validate h1 (Model left side depth: 1 to h2)
if h1 < 1:
    errors.append(f"Parameter 'h1' = {h1} must be at least 1 meter")
if h1 >= h2:
    errors.append(f"Parameter 'h1' = {h1} must be less than h2 = {h2}")

# Validate h2 (Model right side depth: not less than h1+2, range: h1 to 100)
if h2 < h1 + 2:
    errors.append(f"Parameter 'h2' = {h2} must be at least h1+2 = {h1 + 2}")
if h2 > 100:
    errors.append(f"Parameter 'h2' = {h2} must not exceed 100 meters")

# Validate h3 (Upper part model height: 2-100)
if not (2 <= h3 <= 100):
    errors.append(f"Parameter 'h3' = {h3} must be between 2 and 100 meters")

# Validate h4 (Free part of abutment length: less than h3-2, range: 1 to h3-1)
if h4 < 1:
    errors.append(f"Parameter 'h4' = {h4} must be at least 1 meter")
if h4 >= h3 - 1:
    errors.append(f"Parameter 'h4' = {h4} must be less than h3-1 = {h3-1}")

# Validate f (Distributed load projection: less than d-2, minimum 1m)
if f < 1:
    errors.append(f"Parameter 'f' = {f} must be at least 1 meter")
if f >= d - 2:
    errors.append(f"Parameter 'f' = {f} must be less than d-2 = {d-2}")

# Validate b (Half-width of abutment base: 1-2m)
if not (1 <= b <= 2):
    errors.append(f"Parameter 'b' = {b} must be between 1 and 2 meters")

# Check for errors
if errors:
    print("\nPARAMETER VALIDATION ERRORS:")
    for error in errors:
        print(f"  {error}")
    print("\nCannot proceed with model creation due to parameter validation errors.")
    print("Please correct the parameter values and run the script again.")
    exit(1)
else:
    print("All parameters are valid!")
    print("=" * 60)

#######################################################################
# LUSAS MODEL CREATION
#######################################################################

try:
    print("Starting model creation process...")
    
    # Connect to LUSAS and check if a model is open
    lusas = get_lusas_modeller()

    # Check if a model is open and not saved
    if lusas.existsDatabase() and lusas.db().isModified():
        raise Exception("Save or close the current model before running this code")

    # Create a new model
    filename = "bridge_abutment_model.mdl"
    lusas.newProject("Structural", filename)

    # Get a reference to the model database
    database = lusas.getDatabase()
    lusas.setVisible(True)
    lusas.enableUI(True)
    
    # Set the analysis category & vertical axis
    database.setAnalysisCategory("2D Inplane")
    database.setVerticalDir("Y")

    # Set the unit system
    database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))

    # Initialise the Helpers module
    Helpers.initialise(lusas)  

    # Calculate x_value which is related to the slope.
    x_value = t
    if (h2 + h3 - h4 - h1) != 0:
        x_value = t + ((h2 - h1) / (h2 + h3 - h4 - h1)) * (w - d - s - t)

    print("Creating surfaces...")

    # Model geometry #############################################
    # Surface creation by coordinates - Main soil body (Surface 1):
    # Based on the diagram: from bottom left, across bottom, up right side to h2, 
    # then the complex top profile back to left side
    xs = [0.0, w, w, w-d+b, w-d, w-d-b, x_value, t, 0]
    ys = [0, 0, h2, h2, h2, h2, h2, h1, h1]
    zs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)
    print(f"Main soil surface {surface1.getID()} created.")

    # Surface creation by coordinates - Upper left soil region (Surface 2):
    # The trapezoidal region above the sloped line
    xs = [x_value, w-d-b, w-d, w-d, w-d-s]
    ys = [h2, h2, h2, h2+h3-h4, h2+h3-h4]
    zs = [0, 0, 0, 0, 0]
    surface2 = Helpers.create_surface_by_coordinates(xs, ys, zs)
    print(f"Upper soil region {surface2.getID()} created.")

    # Surface creation by coordinates - Wall/structure region (Surface 3):
    # The right side structure with height h3
    xs = [w-d, w-d, w-d, w-d+f, w, w, w-d+b]
    ys = [h2, h2+h3-h4, h2+h3, h2+h3, h2+h3, h2, h2]
    zs = [0, 0, 0, 0, 0, 0, 0]
    surface3 = Helpers.create_surface_by_coordinates(xs, ys, zs)
    print(f"Wall structure {surface3.getID()} created.")
    # End of model geometry ############################

    # Meshing ##########################################
    print("Creating surface mesh...")
    # Create Surface (shell) mesh
    surfMeshAttr = database.createMeshSurface("Shell Mesh")
    surfMeshAttr.setRegular("QPN8", 0, 0, True)
    # Assign the mesh to the surface on loadcase 1
    surfMeshAttr.assignTo([surface1, surface2, surface3], 1)

    print("Creating line meshes for wall and other lines...")              
    #Surface 1
    surfLines1 = lusas.newObjectSet().add(surface1).addLOF("Lines").getObjects("Line")
    line_mesh_attr = database.createMeshLine("EL 1").setSize("NULL",0.5)
    line_mesh_attr.assignTo(surfLines1, 1)
           
    #Surface 2
    surfLines2 = lusas.newObjectSet().add(surface2).addLOF("Lines").getObjects("Line")
    wall_mesh_attr = database.createMeshLine("wall").setSize("BMI3",0.5)
    line_mesh_attr = database.createMeshLine("EL 1").setSize("NULL",0.5)
    for i, line in enumerate(surfLines2):
        if line.getStartPoint().getX() == w-d-b and line.getEndPoint().getX() == w-d:
            wall_mesh_attr.assignTo(line, 1) 
        elif line.getStartPoint().getX()== w-d and line.getEndPoint().getX() == w-d-b:
            wall_mesh_attr.assignTo(line, 1) 
        else:
            line_mesh_attr.assignTo(line, 1) 
    
    #Surface 3
    surfLines3 = lusas.newObjectSet().add(surface3).addLOF("Lines").getObjects("Line")
    wall_mesh_attr = database.createMeshLine("wall").setSize("BMI3",0.5)
    line_mesh_attr = database.createMeshLine("EL 1").setSize("NULL",0.5)
    for i, line in enumerate(surfLines3):
        if line.getStartPoint().getX() ==w-d or line.getEndPoint().getX()==w-d:
            if line.getStartPoint().getX()!=w-d+f and line.getEndPoint().getX()!=w-d+f:
                wall_mesh_attr.assignTo(line, 1)
            else:
                line_mesh_attr.assignTo(line, 1)  
        else:
            line_mesh_attr.assignTo(line, 1)  

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
    for i, line in enumerate(surfLines1):
        if line.getStartPoint().getY() == 0.0 and line.getEndPoint().getY()== 0.0:
            fix_xy_support_attr.assignTo (line,1) 
        elif line.getStartPoint().getX() == 0.0 and line.getEndPoint().getX()== 0.0:
            fix_x_support_attr.assignTo(line,1)
        elif line.getStartPoint().getX() == w and line.getEndPoint().getX()== w:
            fix_x_support_attr.assignTo(line,1) 

    for i, line in enumerate(surfLines3):
        if line.getStartPoint().getX() == w and line.getEndPoint().getX()== w:
            fix_x_support_attr.assignTo (line,1)   
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
    K0 = 0.384              # Coefficient of earth pressure

    material_attr = database.createIsotropicMaterial(soil_name, E_mod, nu, density)
    material_attr.setValue("alpha", alpha)
    material_attr.addPlasticModifiedMohrCoulomb("No", friction, dilatancy, 0, dmpfactor)
    material_attr.addModifiedMohrCoulombCohesion(0, cohesion)
    # Ko Initialisation
    material_attr.addKoElasticRow(0.0, K0)

    # Assign material to the surfaces on loadcase 1
    material_attr.assignTo([surface1, surface2, surface3], 1)
    
    print("Creating concrete material...")
    # Abutment - Create concrete material attribute with properties
    name = "Concrete"
    E_mod = 14.0E6          # Young's modulus
    nu = 0.2                # Poisson's ratio
    density = 2.4           # Density
    alpha = 10.0E-6         # Coefficient of thermal expansion
    concrete_material_attr = database.createIsotropicMaterial(name, E_mod, nu, density)
    concrete_material_attr.setValue("alpha", alpha)
    
    # Assign material to the lines on loadcase 1
    for i, line in enumerate(surfLines2):
        if line.getStartPoint().getX() == w-d-b and line.getEndPoint().getX() == w-d:
            concrete_material_attr.assignTo(line, 1) 
        elif line.getStartPoint().getX()== w-d and line.getEndPoint().getX() == w-d-b:
            concrete_material_attr.assignTo(line, 1) 
        
    for i, line in enumerate(surfLines3):
        if line.getStartPoint().getX() ==w-d or line.getEndPoint().getX()==w-d:
            if line.getStartPoint().getX()!=w-d+f and line.getEndPoint().getX()!=w-d+f:
                concrete_material_attr.assignTo(line, 1)
    # End of Material #################################

    # Geometric #######################################
    print("Creating geometric attributes...")
    # Create a geometric attribute
    geomAttr = database.createGeometricLine("Beam Geometry")
    geomAttr.setValue("elementType", "3D Thick Beam")
    geomAttr.setFromLibrary("UK Sections", "Universal Beams (BS4)", "406x178x74kg UB", 0, 0, 0)
    # Assigning
    for i, line in enumerate(surfLines2):
        if line.getStartPoint().getX() == w-d-b and line.getEndPoint().getX() == w-d:
            geomAttr.assignTo(line, 1) 
        elif line.getStartPoint().getX()== w-d and line.getEndPoint().getX() == w-d-b:
            geomAttr.assignTo(line, 1) 
        
    for i, line in enumerate(surfLines3):
        if line.getStartPoint().getX() ==w-d or line.getEndPoint().getX()==w-d:
            if line.getStartPoint().getX()!=w-d+f and line.getEndPoint().getX()!=w-d+f:
                geomAttr.assignTo(line, 1)
    # End of geometric #####################

    # Loading ##############################
    print("Creating loading attributes...")
    # Create Distributed load
    distrType = "Length"    # Load distribution type: "Total" for total load, "Length" for length distribution, "Area" for area distribution
    wx = 0.0                # Load in X direction
    wy = -10.0              # Load in Y direction

    distrLoadAttr = database.createLoadingGlobalDistributed("GlbD2")
    distrLoadAttr.setGlobalDistributed(distrType, wx, wy)

    # Assignment
    distrLoadAttr.assignTo(surfLines3[2], 1)
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
    print(f"Surface 1 ID: {surface1.getID()}")
    print(f"Surface 2 ID: {surface2.getID()}")
    print(f"Surface 3 ID: {surface3.getID()}")

    # Start analysis
    print("Starting analysis...")
    database.getAnalysis("Analysis 1").solve(False)
    database.openAllResults(False)
    print("Analysis started. Check LUSAS for progress.")
    
    print("\nBridge abutment model created and analysis started successfully.")

except Exception as e:
    print(f"Error creating model: {str(e)}")
    print("\nFailed to create bridge abutment model.")