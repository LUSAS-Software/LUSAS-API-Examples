# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      23_Coupled_Structural_Thermal_Analysis.py
# Description:  Creates coupled Thermal-Structural analysis in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

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

## Set coupling options
database.options().setString("Coupling Type", "Thermal", False, "")
database.options().setString("Coupling Method", "Time", False, "")
database.options().setDouble("Coupling Write Start", 1e-3, False, "")
database.options().setDouble("Coupling Read Start", 1e-3, False, "")
database.options().setBoolean("Initialise Reference Temperatures", True, False, "")

# Get all loadcases (a loadcase is a type of loadset)
loadcases : list['IFLoadcase'] = database.getLoadsets("Loadcase")

# Find first structural loadcase
structLoadcase : 'IFLoadcase' = None
for loadcase in loadcases:
    if loadcase.getAnalysis() != structAnalysis:
        continue
    structLoadcase = loadcase
    break

# Find first thermal loadcase
thermalLoadcase : 'IFLoadcase' = None
for loadcase in loadcases:
    if loadcase.getAnalysis() != thermalAnalysis:
        continue
    thermalLoadcase = loadcase
    break

# Set structural analysis transient control options
structLoadcase.setTransientControl(0)
control = structLoadcase.getTransientControl()
control.setValue("CouplingReadInterval", 1.0).setValue("CouplingWriteInterval", 1.0)
control.setNonlinearManual()
control.setValue("AllowStepReduction", True).setValue("MaxStepReduction", 5)
control.setTimeDomainConsolidation(50e6) # Initial time step
control.setValue("TimeStepRestrictionFactor", 1.0)
control.setValue("MinTimeStepFactor", 0.0)
control.setValue("MaxTimeStepFactor", 100.0E6)
control.setValue("TotalResponseTime", 100.0E6)
control.setValue("MinTimeStep", 0.0)
control.setValue("PoreWaterPressureStep", 0.0)
control.setValue("SaturationStep", 0.0)
control.setValue("MaxExcessPoreWP", 0.0)
control.setValue("rateChangePoreWP", 0.0)
control.setValue("rateChangeSaturation", 0.0)
control.setConstants().setValue("nit", 12)
control.setValue("nalps", 2)
control.setValue("toline", 0.75)
control.setValue("rmaxal", 100.0E6)
control.setValue("rnoral", 100.0E6)
control.setValue("dlnorm", 1.0)
control.setValue("rlnorm", 0.1)
control.setValue("wlnorm", 100.0E6)
control.setValue("dtnrml", 1.0)
control.setValue("ampmx", 5.0)
control.setValue("etmxa", 25.0)
control.setValue("etmna", 0.0)
control.setValue("alpha", 0.0)
control.setValue("beta", 1.0)
control.setValue("gamma", 0.5)
control.setValue("isilcp", False)
control.setValue("pnrm", 0.1)
control.setValue("ptnrm", 0.0)
control.setValue("tnorm", 0.0)
control.setValue("pnorm", 0.0)
control.setValue("GroundwaterSolutionType", "Auto")
control.setValue("PermeabilityType", "Auto")
control.setValue("iterStrategyType", "Auto")
control.setValue("iterDataType", "auto")
control.setOutput().setValue("IncrementIntervalForLusas", 1)
control.setValue("IncrementIntervalForPlotFile", 1)
control.setValue("IncrementIntervalForRestart", 0)
control.setValue("MaxRestartDumpsSaved", 0)
control.setValue("IncrementIntervalForTimeStepLog", 1)
control.setValue("IncrementIntervalForHistory", 1)

# Set thermal analysis transient control options
thermalLoadcase.setTransientControl(0)
control = thermalLoadcase.getTransientControl()
control.setValue("CouplingReadInterval", 1.0)
control.setValue("CouplingWriteInterval", 1.0)
control.setNonlinearManual()
control.setValue("AllowStepReduction", True)
control.setValue("MaxStepReduction", 5)
control.setTimeDomainThermal(50e6) # Initial time step
control.setValue("TimeStepRestrictionFactor", 1.0)
control.setValue("MinTimeStepFactor", 0.0)
control.setValue("MaxTimeStepFactor", 100.0E6)
control.setValue("TotalResponseTime", 100.0E6)
control.setValue("MinTimeStep", 0.0)
control.setConstants().setValue("nit", 12)
control.setValue("nalps", 2)
control.setValue("toline", 0.75)
control.setValue("rmaxal", 100.0E6)
control.setValue("rnoral", 100.0E6)
control.setValue("dlnorm", 1.0)
control.setValue("rlnorm", 0.01)
control.setValue("wlnorm", 100.0E6)
control.setValue("dtnrml", 0.01)
control.setValue("ampmx", 5.0)
control.setValue("etmxa", 25.0)
control.setValue("etmna", 0.0)
control.setValue("alpha", 0.0)
control.setValue("beta", 1.0)
control.setValue("gamma", 0.5)
control.setValue("isilcp", False)
control.setValue("pnrm", 0.1)
control.setValue("ptnrm", 0.0)
control.setValue("tnorm", 0.0)
control.setValue("pnorm", 0.0)
control.setValue("GroundwaterSolutionType", "Auto")
control.setValue("PermeabilityType", "Auto")
control.setValue("iterStrategyType", "Auto")
control.setValue("iterDataType", "auto")
control.setOutput().setValue("IncrementIntervalForLusas", 1)
control.setValue("IncrementIntervalForPlotFile", 1)
control.setValue("IncrementIntervalForRestart", 0)
control.setValue("MaxRestartDumpsSaved", 0)
control.setValue("IncrementIntervalForTimeStepLog", 1)
control.setValue("IncrementIntervalForHistory", 1)
