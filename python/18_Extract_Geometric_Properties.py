# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      18_Extract_Geometric_Properties.py
# Description:  Extract geometric properties of lines (beams) and surfaces.
# Author:       Finite Element Analysis Ltd
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
import csv

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# To successfully run this example you must have a model open (e.g. the model generated from example 15).
# Throw error if no model is open:
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.database()


# Get all lines in the model
all_lines : list["IFLine"] = database.getObjects("Line")

# Filter lines to keep only those with at least one geometric assignment
lines = [line for line in all_lines if len(line.getAssignments("Geometric")) > 0]
print(f"Found {len(lines)} lines with geometric assignments out of {len(all_lines)} total lines")

# Array of cached data to print in csv
csv_data = []

# Print geometric properties of each line
if len(lines) > 0:
    # Header
    header = ["Line ID", "Length", "Section", "Area", "Iyy", "Izz"]
    csv_data.append(header)
    print(", ".join(header))

    for line in lines:
        # Get assigned geometric attribute
        geomAttr : "IFGeometric" = line.getAssignments("Geometric")[0].getAttribute()
        
        # Get geometric properties
        length = line.getLineLength()
        section = geomAttr.getName()
        area = geomAttr.getValue("A")
        Iyy = geomAttr.getValue("Iyy")
        Ixx = geomAttr.getValue("Izz")
        
        # Cache and print the data
        l_data = [line.getID(), length, section, area, Iyy, Ixx]
        csv_data.append(l_data)
        print(", ".join(map(str, l_data)))

        # To see all the supported geometric properties, uncomment the next line:
        # print(geomAttr.getValueNames())


# Get all surfaces in the model
all_surfs : list["IFSurface"] = database.getObjects("Surface")

# Filter surfaces to keep only those with at least one geometric assignment
surfs = [surf for surf in all_surfs if len(surf.getAssignments("Geometric")) > 0]
print(f"Found {len(surfs)} surfaces with geometric assignments out of {len(all_surfs)} total surfaces")

# Print geometric properties of surfaces
surface_data = []
if len(surfs) > 0:
    # Header
    header = ["Surface ID", "Area", "Thickness"]
    csv_data.append(header)
    print(", ".join(header))

    for surf in surfs:
        # Get assigned geometric attribute
        geomAttr : "IFGeometric" = surf.getAssignments("Geometric")[0].getAttribute()
        
        # Get geometric properties
        area = surf.getArea()
        t = geomAttr.getValue("t")
        
        # Cache and print the data
        l_data = [surf.getID(), area, t]
        csv_data.append(l_data)
        print(", ".join(map(str, l_data)))

        # To see all the supported geometric properties, uncomment the next line:
        # print(geomAttr.getValueNames())

# Extract to excel
if len(csv_data) > 0:
    # Ask user if they want to create CSV files
    create_csv = input("\nWould you like to save the data to CSV files? (y/n): ").lower().strip()

    if create_csv in ['y', 'yes']:
        # Create CSV for lines if we have line data
        with open('geometric_properties.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in csv_data:
                writer.writerow(row)
        
        print("Data saved to 'geometric_properties.csv'")
