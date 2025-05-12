# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      20_Create_and_Run_Analyses_and_loadcases.py
# Description:  Creates analyses, loadcases and solves them in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

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
# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)
loadcases = Helpers.get_Analysis_Loadcases(structAnalysis)
# TODO: In v22.0 the Helpers function is not needed anymore, as the analysis.getLoadcases() method is available in the API
#loadcases : list['IFLoadcase'] = structAnalysis.getLoadcases()

# Print loadcase names
print(f"Analysis {structAnalysis.getName()} loadcases:")
for loadcase in loadcases:
    print(f" - {loadcase.getID()}: {loadcase.getName()}")


######################################################
## Solve structural analysis

database.getAnalysis(analysisName).solve(False)

# Open available results
database.openAllResults(False)
