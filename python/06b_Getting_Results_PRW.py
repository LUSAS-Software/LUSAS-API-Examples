# LUSAS API (LPI) PYTHON EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      06b_Getting_Results_PRW.py
# Description:  Extract results from the running LUSAS model using a Print Results Wizard (PRW)
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.db()

# To successfully run the code below you must have a model solved.

# Script results parameters
prw_name = "Shell Results With Global Transform"
export_dir = "C:\Temp\\"

######################################################
## Create a print results wizard for thick shell element results

# Shell Results
attr = database.createPrintResultsWizard(prw_name)

# PRW Settings
attr.setResultsType("Components")
attr.setResultsOrder("Mesh")
attr.setResultsContent("Tabular")
attr.setResultsEntity("Force/Moment - Thick Shell")
attr.setExtent("Elements showing results", "")
attr.setResultsLocation("ElementNodal")
attr.setLoadcasesOption("Active") # Active loadset only
# Target Components
components = ["Nx","Ny","Nxy","Mx","My","Mxy","Sx","Sy"]
attr.setComponents(components)

attr.setResultsTransformGlobal()
attr.showCoordinates(True)
attr.showExtremeResults(False)
attr.setSlice(False)
attr.setAllowDerived(False)
attr.setDisplayNow(False)
attr.setDecimalPlaces(3)
attr.setThreshold(1e-6)

# Release the attribute object (for the shake of this example)
# This variable can later be used instead of the "prwAttr" (provided that it not dereferenced with this command).
attr = None 


######################################################
# Export the results defined by the Print Results Wizard

# Get the Print Results Wizard attribute object
genericAttr : 'IFAttribute' = database.getAttribute("Print Results Wizard", prw_name)
# Note the getAttribute function returns the IFAttribute base class and so we need to cast this to the IFResultsWizard type in order to call the showResults() function
prwAttr : 'IFPrintResultsWizard' = win32.CastTo(genericAttr, "IFPrintResultsWizard")

# Display the table of results
table = prwAttr.showResults()
# Save the grid view to a file
table.saveAs(f"{export_dir}{prw_name}_results.xls", "Microsoft Excel")
table.saveAs(f"{export_dir}{prw_name}_results.txt", "Text")
table.close()
