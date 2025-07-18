# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      20_Create_and_Run_Analyses_and_loadcases.py
# Description:  Creates analyses, loadcases and solves them in the running LUSAS model
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

database = lusas.db() # Save database in variable


######################################################
## Create new structural analysis

analysisName = "New Structural Analysis"
structAnalysis = database.createAnalysisStructural(analysisName, True)

# Create additional loadcase in the analysis
newLoadcase = database.createLoadcase("Self-weight", analysisName)
# Enable gravity in self-weight loadcase
newLoadcase.addGravity(True)
newLoadcase.setGravityFactor(1.0)

# Get list of loadcase objects from analysis
loadcases : list['IFLoadcase'] = structAnalysis.getLoadcases()

# Print loadcase names
print(f"Analysis {structAnalysis.getName()} loadcases:")
for loadcase in loadcases:
    print(f" - {loadcase.getID()}: {loadcase.getName()}")


######################################################
## Solve structural analysis

database.getAnalysis(analysisName).solve(False)

# Open available results
database.openAllResults(False)
