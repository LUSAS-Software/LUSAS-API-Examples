# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      12_Create_and_assign_material.py
# Description:  Creates and assigns materials in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Initialise
Helpers.initialise(lusas) # Initialise the Helpers module
database = lusas.db() # Save database in variable


######################################################
## Create line to use in this example

# Create line
line1 = Helpers.create_line_by_coordinates(0.0, 3.0, 0.0, 3.0, 3.0, 0.0)
# To get existing line, use the following command instead:
# line1 = database.getObject("line", 1) #get line with ID 1

# Create vertical surface
surface1 = Helpers.sweep_lines([line1], [0, 0, 1])
# To get existing surface, use the following command instead:
# surface1 = database.getObject("surface", 1) #get surface with ID 1


######################################################
## Create Isotropic Steel Material

# Create steel material attribute with properties (in model units)
name = "Steel"
E_mod = 210.0E9 # Young's modulus
nu = 0.3 # Poisson's ratio
density = 7849.13 # Density
alpha = 0.000012 # Coefficient of thermal expansion
steel_material_attr = database.createIsotropicMaterial(name, E_mod, nu, density)
steel_material_attr.setValue("alpha", alpha)

# Print material properties acquired from attribute
print(f"Material {name} properties:")
print(f" - E: {steel_material_attr.getValue('E')}")
print(f" - nu: {steel_material_attr.getValue('nu')}")
print(f" - density: {steel_material_attr.getValue('density')}")
print(f" - alpha: {steel_material_attr.getValue('alpha')}")

######################################################
## Create Isotropic Steel Material from Library

name = "Steel from library"

# Copy created steel material
steel_material_attr2 : IFMaterialIsotropic = steel_material_attr.createCopy(name)

# Set library details on material (so that it is recognised as a library material) as values saved on the attribute
steel_material_attr2.setDefinitionMenuID(1, isRelativeID=True) # Set the material library dialog as the attribute editing dialog
steel_material_attr2.setDescription("Ungraded | Steel - Structural | EN1993-1-1:2005") # Attribute description (optional)
steel_material_attr2.createValue("Region", 0, 0, 0, 0, 0, 0, 0).setValue("Region", "UK")
steel_material_attr2.createValue("Standard", 0, 0, 0, 0, 0, 0, 0).setValue("Standard", "EN1993-1-1:2005")
steel_material_attr2.createValue("Material", 0, 0, 0, 0, 0, 0, 0).setValue("Material", "Steel - Structural")
steel_material_attr2.createValue("Grade", 0, 0, 0, 0, 0, 0, 0).setValue("Grade", "Ungraded")

# Assign material to the line on loadcase 1
steel_material_attr2.assignTo(line1, 1)


######################################################
## Create Isotropic Concrete Material from Library

# Create concrete material attribute with properties (in model units)
name = "Concrete from library"
E_mod = 35.0E9 # Young's modulus
nu = 0.2 # Poisson's ratio
density = 2.54842E3 # Density
alpha = 10.0E-6 # Coefficient of thermal expansion
concrete_material_attr = database.createIsotropicMaterial(name, E_mod, nu, density)
concrete_material_attr.setValue("alpha", alpha)

# Optionally, set library details on material (so that it is recognised as a library material) as values saved on the attribute
concrete_material_attr.setDefinitionMenuID(1, isRelativeID=True)
concrete_material_attr.setDescription("C40/50 | Concrete | EN1992-1-1:2004/2014")
concrete_material_attr.createValue("Grade").setValue("Grade", "C40/50")
concrete_material_attr.createValue("Region").setValue("Region", "Europe")
concrete_material_attr.createValue("Standard").setValue("Standard", "EN1992-1-1:2004/2014")
concrete_material_attr.createValue("Material").setValue("Material", "Concrete")
concrete_material_attr.createValue("ec3").setValue("ec3", 1.75E-3)
concrete_material_attr.createValue("fcd3", 0, 1, -2, 0, 0, 0, 0).setValue("fcd3", 26.66666667E6)
concrete_material_attr.createValue("fck", 0, 1, -2, 0, 0, 0, 0).setValue("fck", 40.0E6)
concrete_material_attr.createValue("fctm", 0, 1, -2, 0, 0, 0, 0).setValue("fctm", 3.5E6)
concrete_material_attr.createValue("ecu3").setValue("ecu3", 3.5E-3)
concrete_material_attr.createValue("E3", 0, 1, -2, 0, 0, 0, 0).setValue("E3", 15.238095238E9)
# Optionally, add descriptions to the values
concrete_material_attr.setValueDescription("ec3", "Compressive strain limit 3", False)
concrete_material_attr.setValueDescription("fcd3", "Design compressive strength 3", False)
concrete_material_attr.setValueDescription("fck", "Characteristic compressive cylinder strength of concrete at 28 days", False)
concrete_material_attr.setValueDescription("fctm", "Mean value of axial tensile strength of concrete", False)
concrete_material_attr.setValueDescription("ecu3", "Ultimate compressive strain limit 3", False)
concrete_material_attr.setValueDescription("E3", "Modulus of elasticity 3", False)

# Assign material to the surface on loadcase 1
concrete_material_attr.assignTo(surface1, 1)
