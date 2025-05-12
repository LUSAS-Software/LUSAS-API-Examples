# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      32_User_Defined_Results_and_Design_Attributes.py
# Description:  Create User Defined Results and Design Attributes in the running LUSAS model.
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


# User defined results are formulae that can be evaluated using model parameters such as geometric and material attribute values
# as well as load effects from the analysis allow new results to be displayed in any LUSAS results processing tools (Contours, Reports, Diagrams etc).

# In this example we will create a user defined result to:
# - calculate the top and bottom stresses for concrete beams,
# - determine if the section is cracked based on the set concrete grade.
#
# For the purpose of this example, a simply supported concrete beam is modelled, so make sure you use an empty model before running this script.


######################################################
## Create a simply supported concrete beam to use in this example

# Set units to N and m
database.setModelUnits(lusas.getUnitSet("N,m,kg,s,C"))
# Create a new line in the model
line1 = Helpers.create_line_by_coordinates(0.0, 1.0, 0.0, 5.0, 1.0, 0.0)
# Mesh
database.createMeshLine("Beam Mesh").setSize("BMI21", 1).assignTo(line1, 1)
database.updateMesh()
# Rectangular section
database.createParametricSection("Sct1").setType("Rectangular Solid").setDimensions(["B", "D"], [0.4, 0.6])
paramSection = database.createGeometricLine("LGeo1").setFromLibrary("Utilities", "", "Sct1", 0, 0, 0)
paramSection.setValue("elementType", "3D Thick Beam")
paramSection.assignTo(line1, 1)
# Concrete material
database.createIsotropicMaterial("Concrete", 35.0E9, 0.2, 2.54842E3).assignTo(line1, 1)
# Pin supports at line ends
database.createSupportStructural("Pinned").setStructural("R", "R", "R", "F", "F", "F").assignTo(lusas.newObjectSet().add([line1.getStartPoint(), line1.getEndPoint()]), 1)
# UDL
database.createLoadingGlobalDistributed("GlbD1").setGlobalDistributed("Length", 0, 0, -4000 * 2).assignTo(line1, 1)


####################################################################
# Create the User Defined Results (UDR) expressions
# (Can be done through the UI by navigating to Utilities > User Defined Results...)

# Create the user defined results attribute to store all the expressions
# These new results (output of each expression) will be available along with all the other results in Contours, Reports, Diagrams etc.
user_defined_results = database.createUserDefinedResult("User-defined")

# Top and bottom stresses are added to the existing force/moment entity to access the correct results entity, i,e My or a thick beam
user_defined_results.setUserResultComponent("s_top", "Force/Moment - Thick 3D Beam", "Fx / geometric.A + My / geometric.Szt", "Stress_top")
user_defined_results.setUserResultComponent("s_bot", "Force/Moment - Thick 3D Beam", "Fx / geometric.A + My / geometric.Szb", "Stress_bottom")
# Note geometric refers to the assigned geometric (section) attribute. Szb is the section modulus at the negative z axis and is negative

# You can also create new entities instead of adding the results under "Force/Moment - Thick 3D Beam",
# for example, we can group all our concrete cracking results (max_fct, isCracked etc) in a new entity named "Concrete Cracking"
results_entity = "Concrete Cracking"
database.addUserDefinedResultsEntity(results_entity, "Thick 3D Beam")
# maximum tensile stress in top and bottom fibres
user_defined_results.setUserResultComponent("max_fct", results_entity, "max(s_top, s_bot)", "Max tensile stress")


####################################################################
# Create and use Design attributes in UDRs
# To assess if the concrete section is cracked, we will need to compare the tensile stresses with the tensile strength fctm of the concrete.
# To allow for different concrete grades, we will create design attributes for each concrete grade, which can then be assigned on concrete beams.

# Dictionary with concrete tensile strength fctm per concrete type (EN1992-1-1)
fctm_dict = dict() # values in MPa
fctm_dict["C20/25"] = 2.21
fctm_dict["C25/30"] = 2.56
fctm_dict["C30/37"] = 2.90
fctm_dict["C35/45"] = 3.21
fctm_dict["C40/50"] = 3.51

# Get units objects used for conversions
mpa_units_object = lusas.getUnitSet("N,mm,t,s,C") # MPa units = N/mm²
model_units_object = database.getModelUnits()

# Create fctm design attributes for each concrete type
for concrete_type, fctm in fctm_dict.items():
    # Create a design attribute for the concrete type
    attr_type = "Concrete Cracking" # The attribute will be created under the "Concrete Design" tree view category
    attr_scope = "concrete_cracking" # This is used to access the design attribute values in the UDR expressions
    assign_type = "Lines" # Can be assigned on Lines
    fctm_attr = database.createDesignAttribute(f"fctm {fctm} MPa", attr_type, attr_scope, assign_type)
    # Set the concrete type as the description of the design attribute, this will be shown in the UI next to the design attribute name
    fctm_attr.setDescription(concrete_type)
    
    # Convert the tensile strength into model units
    # Dimensionality: MPa = N/mm² = force ^ 1 and length ^ -2
    fctm_in_model_units = mpa_units_object.convertToUnitSet(model_units_object, fctm, 0, 1, -2, 0, 0, 0)
    # Print value in converted units to the console
    print(f"fctm = {fctm_in_model_units} {model_units_object.getForceShortName()}/{model_units_object.getLengthShortName()}² ({concrete_type})")
    
    # Save the tensile strength on the design attribute
    fctm_attr.createValue("fctm", 0, 1, -2, 0, 0, 0) # create the value with the correct units (setting the units is optional)
    fctm_attr.setValue("fctm", fctm_in_model_units)

# Assign first design attribute to the line (beam) element
database.getAttribute("Design", "fctm 2.21 MPa").assignTo(line1, 1)


## Create User Defined Result that read the design attribute fctm values and calculate if the section is cracked:

# Set UDR options to disable variable checking when model has no design assignments yet
opt = lusas.newUDROptions()
opt.setErrorCheckingLevel("NoVars")

# - fctm UDR
# To avoid errors on elements that do not have a design attribute assigned, we can use the "isDefined" function 
# to check if the design.concrete_cracking.fctm exists (design attribute is assigned). If it does not exist the UDR will return no value using the "none()" function.
user_defined_results.setUserResultComponent("udr_fctm", results_entity, f"if (isDefined(design.{attr_scope}.fctm), design.{attr_scope}.fctm, none())", "Tensile capacity", opt)

# - isCracked UDR
# Determine if the stress exceeds the tensile limit
# Mind that when the UDR "fctm" returns the "none()" function, that value is almost 0. So we should manually check if the design.concrete_cracking.fctm
# exists to avoid assuming fctm is 0.
# In this case, once again we will return the "none()" function, so that modeller does not show the result.
user_defined_results.setUserResultComponent("isCracked", results_entity, f"if (isDefined(udr_fctm), if(max_fct > udr_fctm, 1, 0), none())", "1 = cracked, 0 = not cracked")


# It should be noted that instead of manually creating design attributes for each concrete type,
# we could have read the fctm value directly from the assigned material!
# To do so, we would have to use the "material.fctm" scope value instead of the "design.concrete_cracking.fctm" in all the above UDR expressions.
# For this to work, the used concrete material should be created from the material library with the Standard set to Eurocode 2.
# To explore other values that can be read from the materials or other attributes, use the "attribute.getValueNames()" method.


####################################################################
# Solve and set the contour layer to show the user defined result "isCracked" with a two tone contour plot

database.getAnalysis("Analysis 1").solve(False)
database.openAllResults(False)

# Add the contours layer to the view if it does not exist
if not lusas.view().existsContoursLayer():
    lusas.view().insertContoursLayer()
lusas.view().contours().setResults("Concrete Cracking", "isCracked")
lusas.view().contours().chooseSettings(4)
