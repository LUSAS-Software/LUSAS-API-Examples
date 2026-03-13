# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      412 Free Cantilever Method model.py
# Author:       Finite Element Analysis Ltd
# Description:  Spline model of a bridge using the LUSAS free cantilever method (FCM) wizard.
#               This example shows how to use the FCM wizards to generate a model of a bridge.
#               The FCM data is stored in a JSON file and loaded onto the bridge data utility.
#               The FCM wizard is then launched to generate the model based on the data.
#######################################################################

# Add parent directory to sys.path so that we can load libraries from the parent directory
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(parent_dir)

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

#=======================================================================
# Parameters

filename = "fcm_bridge_model.mdl"

# FCM utility data in JSON format
# These data can be extracted from existing FCM utilities using the command (LUSAS v24+):
#   Command bar:    call getExtModule("FcmWizard.LusasEntryPoint").exportToFile("filename")
#   Python:         lusas.getExtModule("FcmWizard.LusasEntryPoint").exportToFile("filename")
dataPathJSON = "412 FCM_data.json"

#=======================================================================
# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Check if a model is open and not saved
if lusas.existsDatabase() and lusas.db().isModified():
    raise Exception("Save or close the current model before running this code")

# Create a new model
lusas.newProject("Structural", filename)

# Get a reference to the model database
database = lusas.getDatabase()
lusas.setVisible(True)
lusas.enableUI(True)

# Set the analysis category & vertical axis
database.setAnalysisCategory("3D")
database.setVerticalDir("Z")

# Set the unit system
database.setModelUnits(lusas.getUnitSet("kN,m,t,s,C"))
database.setTimescaleUnits("days") # Required by the FCM wizard

#=======================================================================
# Create attributes and utilities used in the bridge data

# Materials
concreteC35 = database.createIsotropicMaterial("C35", 34.0E9, 0.2, 2.5484E3)
concreteC35.addEurocodePlasticMaterial86(0.0, 0.0)
concreteC35.addEurocode2ConcreteCreep(35.0E6, "class N", 70.0, 0.0, False, 1.0, True, 1, 0.0)
concreteC35.addEurocode2ConcreteShrinkage(True)
concreteC35.renumber(1)

concreteC40 = database.createIsotropicMaterial("C40", 35.0E9, 0.2, 2.5484E3)
concreteC40.addEurocodePlasticMaterial86(0.0, 0.0)
concreteC40.addEurocode2ConcreteCreep(40.0E6, "class N", 70.0, 0.0, False, 1.0, True, 1, 0.0)
concreteC40.addEurocode2ConcreteShrinkage(True)
concreteC40.renumber(2)

# Sections
# Pier section utility
pierSct = database.createParametricSection("Rec")
pierSct.setType("Rectangular Solid")
dims = {"B": 8.1, "D": 1.8}
pierSct.setDimensions(list(dims.keys()), list(dims.values()))
pierSct.setTreeLocation("Rectangular Sections")
pierSct.renumber(1)
# geometric attribute
attr = database.createGeometricLine("Pier")
attr.setValue("elementType", "3D Thick Beam")
attr.setFromLibrary("Utilities", "", "Rec", 0, 0, 0)
attr.renumber(1)

# At Pier section utility
atPierSct = database.createParametricSection("At Pier")
atPierSct.setType("Complex Box (Camber, Single Cell)")
dims = {
    "n":   1.0,  "Wt":  3.55, "Wb":  3.55, "H":   7.0,  "Wc":  2.8,
    "Tc1": 0.6,  "Tc2": 0.25, "Hm":  0.0,  "Tt":  0.25, "Tb":  0.85,
    "nt":  1.0,  "nb":  1.0,  "nc":  1.0,  "ni":  0.0,  "ne":  0.0,
    "OP1": 3.1,  "HP1": 0.575,"OP2": 3.1,  "HP2": 1.1,
    "Ot1": 1.35, "Ht1": 0.25, "Ob1": 1.85, "Hb1": 0.85,
    "Oc1": 1.05, "Hc1": 0.25,
}
atPierSct.setDimensions(list(dims.keys()), list(dims.values()))
atPierSct.setTreeLocation("Box Sections")
atPierSct.renumber(2)
# geometric attribute
attr = database.createGeometricLine("At Pier box")
attr.setValue("elementType", "3D Thick Beam")
attr.setFromLibrary("Utilities", "", "At Pier", 0, 0, 0)
attr.setValue("ez0", 3.72, 0)
attr.renumber(2)

# Midspan section utility
midspanSct = database.createParametricSection("midspan")
midspanSct.setType("Complex Box (Camber, Single Cell)")
dims = {
    "n":   1.0,  "Wt":  3.55, "Wb":  3.55, "H":   2.7,  "Wc":  2.8,
    "Tc1": 0.6,  "Tc2": 0.25, "Hm":  0.0,  "Tt":  0.25, "Tb":  0.26,
    "nt":  1.0,  "nb":  1.0,  "nc":  1.0,  "ni":  0.0,  "ne":  0.0,
    "OP1": 3.1,  "HP1": 0.575,"OP2": 3.1,  "HP2": 0.51,
    "Ot1": 1.35, "Ht1": 0.25, "Ob1": 1.85, "Hb1": 0.26,
    "Oc1": 1.05, "Hc1": 0.25,
}
midspanSct.setDimensions(list(dims.keys()), list(dims.values()))
midspanSct.setTreeLocation("Box Sections")
midspanSct.renumber(3)
# geometric attribute
attr = database.createGeometricLine("midspan2")
attr.setValue("elementType", "3D Thick Beam")
attr.setFromLibrary("Utilities", "", "midspan", 0, 0, 0)
attr.setValue("ez0", 1.05553, 0)
attr.renumber(3)

# Tendon Properties utility
attr = database.createTendonProperties("Prp1")
attr.setDesignCode("EN1992-1-1:2004 / 2014 Eurocode 2", True)
attr.setValue("elasticShort", 0)
attr.setValue("shortAvg", -1.0)
attr.setValue("diameter", 72.3)
attr.setValue("modulus", 195.0E6)
attr.setValue("wobbleFactor", 0.01)
attr.setValue("friction", 0.19)
attr.setValue("lossType", 1)
attr.setValue("tensileS", 1.86E3)
attr.setValue("characteristicProof", 1.675E3)
attr.setValue("relaxClass", 2)
attr.setValue("loss", 2.5)
attr.renumber(1)

#=======================================================================
# Create the FCM bridge data utility
dataUtility = database.createDesignAttribute("Bridge data", "Free Cantilever Method Wizard", "FCMScope", "", True)
dataUtility.setTreeLocation("Free Cantilever Method Wizard")
# set the EditingMenuID so that user can double click to revisit the dialog of FCM
ID_FCM_WIZARD_DEFINITION = 39511
dataUtility.setEditingMenuID(ID_FCM_WIZARD_DEFINITION, None, None)

# Load FCM data from JSON file as a string
json_file = os.path.join(os.path.dirname(__file__), dataPathJSON)
with open(json_file, "r") as f:
    fcm_data_string = f.read()

# Split the FCM data string into chunks of max 8000 characters and save each on the utility
chunk_size = 8000
fcm_data_parts = [fcm_data_string[i:i + chunk_size] for i in range(0, len(fcm_data_string), chunk_size)]
for i, part in enumerate(fcm_data_parts, start=1):
    if not dataUtility.existsValue(f"FCMSTORE{i}"):
        dataUtility.createValue(f"FCMSTORE{i}")
    dataUtility.setValue(f"FCMSTORE{i}", part)

#=======================================================================
# Generation

try:
    # Get FcmWizard module (needs to be saved as a variable)
    module = lusas.getExtModule("FcmWizard.LusasEntryPoint")
    # Run the FCM generation
    module.RunFcm()
    print("Model building completed successfully!")
except Exception as e:
    print("Error during FCM generation:", e)
    raise
