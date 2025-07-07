# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      01_Connect_to_LUSAS.py
# Description:  Connects on the running LUSAS instance and prints in the log
# Author:       Finite Element Analysis Ltd
# 

# Libraries
import win32com.client as win32

# Connect to a running LUSAS Modeller or create a new instance using the pywin32 module.
lusas = win32.dynamic.Dispatch("Lusas.Modeller.21.1")
# Notes: - To target different LUSAS versions, change the version number e.g from "Lusas.Modeller.22.0" to "Lusas.Modeller.21.1"
#        - If you get the error 'Import "win32com.client" could not be resolved', then the pywin32 Python library is missing.
#          You can install the missing library by running the command "pip install pywin32==308" in the terminal.
#          For more information please refer to the installation guide.

# Ensure modeller is visible
lusas.setVisible(True)

# Print in the LUSAS log to test the connection
lusas.getTextWindow().writeLine("Hello world!")


# To simplify the connection, enable autocomplete and LPI documentation, it is recommended that the LPI module is imported. 
# You can acquire the `lusas` object with the `get_lusas_modeller()` method, while notice that `writeLine()` is now a documented on mouse over
# (if your IDE supports it).

from shared.LPI import *

lusas = get_lusas_modeller()
lusas.getTextWindow().writeLine("Hello world! (LPI module)")


# Print (in python window) the connected model name
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

print("Model name: ", lusas.db().getDBBasename())


# Save and close the open model and LUSAS
if lusas.existsDatabase():
    lusas.project().save()
    lusas.project().close()

# Optionally, close LUSAS
#lusas.quit()