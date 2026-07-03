# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      140 FCM Replace Multiple Varying with Tapered Sections.py
# Author:       Finite Element Analysis Ltd
# Description:  This converts each assigned "Multiple Varying Section" geometric line attribute
#               into a separate two-end tapered geometric line attribute, one per line.
#               Tapered sections allow the definition of reinforcement so that they are used for RC design.
#               The section interpolated dimensions are taken from the elements at the ends of each line,
#               based on the assigned attribute. The same approach can be used to get interpolated properties
#               like thickness, cross sectional properties etc along an element.
#######################################################################

# Add parent directory to sys.path so that we can load libraries from the parent directory
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(parent_dir)

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Get the LUSAS Modeller object
lusas = get_lusas_modeller()

db = lusas.database()

######################################################
### CONFIGURATION
ASSIGN_LOADCASE = 1 # change if your geometric assignments are not on loadcase 1
CAMBER_BOX_SECTION_SINGLE_CELL_DIMENSIONS = ("n", "Wt", "Wb", "H", "Wc", "Tc1", "Tc2", "Hm", "Tt", "Tb", "nt", "nb", "nc", "ni", "ne", "OP1", "HP1", "OP2", "HP2", "Ot1", "Ht1", "Ob1", "Hb1", "Oc1", "Hc1")

# Eccentricity
yType = "Centroid"
zType = "Fibre"
yFibre = ""
zFibre = "B1"

######################################################
### Helper functions

def create_line_end_section(line: IFLine, localCrds: float) -> IFParametricSection:
    """
    Creates a new "Complex Box (Camber, Single Cell)" parametric section based on the dimensions of the element at the given local coordinates along the line.
    Parameters:
        line: The line object to get the element from.
        localCrds: The local coordinates along the line (0 for start, 1 for end).
    Returns:
        The newly created parametric section attribute.
    """
    name = "L{}_{}".format(line.getID(), localCrds)

    # Create a new parametric section attribute
    attr = db.createParametricSection(name)
    # Set the type to "Complex Box (Camber, Single Cell)"
    attr.setType("Complex Box (Camber, Single Cell)")
    
    # Get element at requested line end
    elm: IFElement
    nrmCoordOnElement: float
    elm, nrmCoordOnElement = line.getElementAtNormalisedPosition(localCrds)
    # Get section dimensions from element end
    values = [elm.getAttributeValueAtU(nrmCoordOnElement, "Geometric", key) for key in CAMBER_BOX_SECTION_SINGLE_CELL_DIMENSIONS]
    
    # Update dimensions in created section
    attr.setDimensions(CAMBER_BOX_SECTION_SINGLE_CELL_DIMENSIONS, values)
    
    return attr

######################################################
### Main code

# Check if a model is open
if not lusas.existsDatabase():
    raise Exception("No model is open. Please open a FCM model before running this code.")

# Get all Multiple Varying Geometric attributes
mvg_attrs = db.getAttributes("Multiple Varying Geometric")

if len(mvg_attrs) == 0:
    raise Exception("Model has no Multiple Varying Geometric attributes.")

try:
    # Hide modeller to speed up the process
    lusas.enableUI(False)
    db.beginCommandBatch("Converting Multiple Varying Geometric Attributes to Tapered Sections")
    
    # Start a progress bar to show per attribute progress
    lusas.initStatusBarProgressCtrl("Converting Geometric Attributes", len(mvg_attrs))

    # Loop attributes and replace
    assgnmnt = lusas.newAssignment().setIgnoreAll()
    for mvg_attr in mvg_attrs:
        # Get attribute assigned lines
        lines = lusas.newObjectSet().add(mvg_attr, assgnmnt).getObjects("Line")
        
        # Check if this is a CamberBoxSectionSingleCellE (= 28)
        if mvg_attr.getValue("Type") != 28:
            continue
        
        print("Replacing '{}' in {} lines...".format(mvg_attr.getName(), len(lines)))
        
        # Loop lines and replace
        for line in lines:
            # Create new attribute
            new_name = "{} (L{}_TAPER)".format(mvg_attr.getName(), line.getID())
            new_attr = db.createGeometricLine(new_name)
            new_attr.setNumberOfSections(2)
            
            # Copy values from the Multiple Varying Section attribute to the new tapered section attribute
            new_attr.setValue("elementType", mvg_attr.getValue("elementType"))
            new_attr.setValue("interpMethod", mvg_attr.getValue("interpMethod"))
            
            # Create parametric sections based on line end section dimensions
            start_section = create_line_end_section(line, 0)
            end_section = create_line_end_section(line, 1)

            # Set sections in the new tapered section attribute
            new_attr.setFromLibrary("Utilities", "", start_section.getName(), 0, 0, 0) # Section 1
            new_attr.setFromLibrary("Utilities", "", end_section.getName(), 0, 0, 1) # Section 2
            
            # Set start section eccentricity
            new_attr.setEccentricityOrigin(yType, zType, yFibre, zFibre)
            # Fix eccentricities of second section
            if yType == "Fibre":
                fcZ, fcY = new_attr.getFibrePosition(yFibre, None, None, 1)
                new_attr.setValue("ey0", fcY, 1)
            if zType == "Fibre":
                fcZ, fcY = new_attr.getFibrePosition(zFibre, None, None, 1)
                new_attr.setValue("ez0", fcZ, 1)
            
            # Assign the new tapered section.
            new_attr.assignTo(line, ASSIGN_LOADCASE)
        
        # Update progress bar
        lusas.statusBarProgressCtrlStep()

except Exception as e:
    print("Error: ", e)

finally:
    # Finish progress bar & close command batch
    lusas.unInitStatusBarProgressCtrl()
    db.closeCommandBatch()

    # Ensure modeller is visible at the end of the process
    lusas.enableUI(True)
    