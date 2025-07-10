# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      31_Getting_Results_PRW.py
# Description:  Extract results from the running LUSAS model using a Print Results Wizard (PRW)
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
import os
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.db()

# To successfully run the code below you must have a model solved (e.g. the model generated from example 15).

# Script results parameters
prw_name = "Displacements"
export_dir = os.path.expanduser("~\\Desktop") # export in user desktop

######################################################
## Create a print results wizard for Thick 3D Beam element results

# Shell Results
attr = database.createPrintResultsWizard(prw_name)

# PRW Settings
attr.setResultsType("Components")
attr.setResultsOrder("Mesh")
attr.setResultsContent("Tabular")
attr.setResultsEntity("Displacement")
attr.setExtent("Elements showing results", "")
attr.setResultsLocation("Nodal")
attr.setLoadcasesOption("Active") # Active loadset only
# Target Components
components = ["DX","DY","DZ","THX","THY","THZ","RSLT"]
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
prwAttr : "IFPrintResultsWizard" = database.getAttribute("Print Results Wizard", prw_name)

# Display the table of results
table = prwAttr.showResults()
# Save the grid view to a file
table.saveAs(f"{export_dir}\\{prw_name}_results.xls", "Microsoft Excel")
print(f"Results saved to {export_dir}\\{prw_name}_results.xls")
table.saveAs(f"{export_dir}\\{prw_name}_results.txt", "Text")
print(f"Results saved to {export_dir}\\{prw_name}_results.txt")
table.close()
