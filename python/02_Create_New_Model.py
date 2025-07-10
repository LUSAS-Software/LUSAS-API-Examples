# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      02_Create_New_Model.py
# Description:  Create a new LUSAS model
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Check if a model is open and not saved
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("Save or close the current model before running this code")


# Create a new model
filename = "my_new_model.mdl"
lusas.newProject("Structural", filename)

# Get a reference to the model database
db = lusas.getDatabase()

# Set the analysis category & vertical axis
db.setAnalysisCategory("3D")
db.setVerticalDir("Z")

# Set the unit system
db.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))