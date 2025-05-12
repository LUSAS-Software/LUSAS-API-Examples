# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      22_Create_Combinations_and_Envelopes.py
# Description:  Creates combinations and envelopes in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

database = lusas.db() # Save database in variable

# Check if loadcases 1 and 2 exist (required for this example)
loadcases : list['IFLoadset'] = database.getLoadsets("loadcase")
loadcaseIDs : list[int] = [ls.getID() for ls in loadcases]
if not 1 in loadcaseIDs or not 2 in loadcaseIDs:
    raise Exception("This example assumes that loadcases with ID 1 and 2 exist in the model")


## Create basic combination
basicCombo = database.createCombinationBasic("Basic Combination")
# Add loadcase 1 in the combination with a factor of 1.5
basicCombo.addEntry(1.5, 1) #assumes that loadcase with ID = 1 exists
# Add loadcase 2 in the combination with a factor of 1.0
basicCombo.addEntry(1.0, 2) #assumes that loadcase with ID = 2 exists


## Create smart combination
smartCombo = database.createCombinationSmart("Smart Combination")
# Add loadcase 1 in the combination
beneficialFactor = 0.25
adverseFactor = 1.5
smartCombo.addEntry(beneficialFactor, adverseFactor - beneficialFactor, 1)
# Add loadcase 2 in the combination
beneficialFactor = 0.25
adverseFactor = 1.0
smartCombo.addEntry(beneficialFactor, adverseFactor - beneficialFactor, 2)


## Create envelop combination
envCombo = database.createEnvelope("Test Envelop")
# Add loadcase 1 (using ID)
envCombo.addEntry(1)
# Add loadcase 2 (using ID)
envCombo.addEntry(2)
# Add basic combination (using name)
id = basicCombo.getID()
envCombo.addEntry(id)
# Add smart combination (using object)
envCombo.addEntry(smartCombo)
