# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      15_Simply_Supported_Beam.py
# Description:  Create a simply supported concrete beam.
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Helpers module (easier geometry creation)
import shared.Helpers as Helpers

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if a model is open and not saved
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("This script will create a new model. Please save or close the current model and try again")

# Initialise
Helpers.initialise(lusas) # Initialise the Helpers module


# Create a new model
lusas.newProject("Structural", "Simple_beam_model")
database = lusas.db()

database.setAnalysisCategory("3D")
database.setVerticalDir("Z")

# Set units to N and m
database.setModelUnits(lusas.getUnitSet("N,m,kg,s,C"))

# Create a new line in the model
line1 = Helpers.create_line_by_coordinates(0.0, 1.0, 0.0, 5.0, 1.0, 0.0)

# Mesh
mesh = database.createMeshLine("Beam Mesh").setSize("BMI21", 1).assignTo(line1, 1)
database.updateMesh()

# Rectangular section
database.createParametricSection("Sct1").setType("Rectangular Solid").setDimensions(["B", "D"], [0.4, 0.6])
paramSection = database.createGeometricLine("LGeo1").setFromLibrary("Utilities", "", "Sct1", 0, 0, 0)
paramSection.setValue("elementType", "3D Thick Beam")
paramSection.assignTo(line1, 1)

# Concrete material
database.createIsotropicMaterial("Concrete", 35.0E9, 0.2, 2.54842E3).assignTo(line1, 1)

# Pin supports at line ends
line_ends_objectset = lusas.newObjectSet().add([line1.getStartPoint(), line1.getEndPoint()])
database.createSupportStructural("Pinned").setStructural("R", "R", "R", "F", "F", "F").assignTo(line_ends_objectset, 1)

# Apply UDL
database.createLoadingGlobalDistributed("GlbD1").setGlobalDistributed("Length", 0, 0, -4000 * 2).assignTo(line1, 1)


# Solve and set the contour layer to show the user defined result "isCracked" with a two tone contour plot
database.getAnalysis("Analysis 1").solve(False)
database.openAllResults(False)

# Add the contours layer to the view if it does not exist and set it to deflections
if not lusas.view().existsContoursLayer():
    lusas.view().insertContoursLayer()
lusas.view().contours().setResults("Displacement", "RSLT")
lusas.view().contours().chooseSettings(1)

# Set top-left-front view (isometric)
lusas.view().setIsometric()
