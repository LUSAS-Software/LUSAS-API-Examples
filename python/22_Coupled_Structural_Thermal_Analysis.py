# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      22_Coupled_Structural_Thermal_Analysis.py
# Description:  Creates coupled Thermal-Structural analysis in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

database = lusas.db() # Save database in variable

# it is assumed that only one structural analysis called "Analysis 1" exists in the model
allAnalyses : list['IFAnalysisBaseClass']= database.getAnalyses()
if len(allAnalyses) > 1 or allAnalyses[0].getName() != "Analysis 1":
    raise Exception("This example assumes that only one structural analysis called 'Analysis 1' exists in the model")

# Get the structural analysis
structAnalysis = database.getAnalysis("Analysis 1")

## Create new thermal analysis
thermalAnalysis = database.createAnalysisThermal("Analysis 1 (Thermal)", True, "Nonlinear and transient")
thermalAnalysis.setAsBase()
thermalAnalysis.setUndeformedMeshStart()
thermalAnalysis.setCoupled("Analysis 1")

## Set coupling model options (the options set in the "Couple analysis options" dialog)
# Set the thermal analysis to run first
database.options().setString("Coupling Type", "Thermal", False, "")
# Use first thermal analysis temperatures as reference temperatures in the structural analysis
database.options().setBoolean("Initialise Reference Temperatures", True, False, "")
# Set time to control the coupling steps (instead of increments)
database.options().setString("Coupling Method", "Time", False, "")
# Set time-steps to start read/write the first data (in model units, e.g. seconds)
database.options().setDouble("Coupling Write Start", 1e-3, False, "")
database.options().setDouble("Coupling Read Start", 1e-3, False, "")

# Find first structural loadcase
structLoadcase : 'IFLoadcase' = structAnalysis.getLoadcases()[0]

# Find first thermal loadcase
thermalLoadcase : 'IFLoadcase' = thermalAnalysis.getLoadcases()[0]

# Set structural loadcase nonlinear & transient control options
structLoadcase.setTransientControl(0)               # Add nonlinear & transient control (0 means no time steps limit)
control = structLoadcase.getTransientControl()      # Get created transient control
control.setValue("CouplingReadInterval", 1.0)       # Time between each read (in model units, e.g. seconds)
control.setValue("CouplingWriteInterval", 1.0)      # Time between each write (in model units, e.g. seconds)
control.setNonlinearManual()                        # Set nonlinear incrementation with manual (loading data in each loadcase is specified separately)
control.setTimeDomainConsolidation(50e6)            # Initial time step (in model units, e.g. seconds)
control.setValue("MinTimeStepFactor", 0.0)          # Minimum time step to use (in model units, e.g. seconds)
control.setValue("MaxTimeStepFactor", 100.0E6)      # Maximum time step to use (in model units, e.g. seconds)
control.setValue("TotalResponseTime", 100.0E6)      # Total response time (in model units, e.g. seconds)

# Set thermal loadcase nonlinear & transient control options similarly to the structural loadcase
thermalLoadcase.setTransientControl(0)
control = thermalLoadcase.getTransientControl()
control.setValue("CouplingReadInterval", 1.0)
control.setValue("CouplingWriteInterval", 1.0)
control.setNonlinearManual()
control.setTimeDomainThermal(50e6)
control.setValue("MinTimeStepFactor", 0.0)
control.setValue("MaxTimeStepFactor", 100.0E6)
control.setValue("TotalResponseTime", 100.0E6)
