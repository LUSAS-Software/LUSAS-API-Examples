# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      33_Getting_Results_2D_Slice.py
# Description:  Prints results along a 2D slice and calculates the total resultant and total moment.
#               The total resultant and total moment are calculated through integration using the trapezoidal rule.
# Author:       Finite Element Analysis Ltd
# 

# To successfully run the code below you must have:
# - a compatible model:
#     - a 2D continuum model,
#     - a shell, or a plate model,
#     - a slice section which was cut through a solid model
# - the active loadcase solved
# - a line that passes the target area selected
# Caution: In axisymmetric models, the variable transverse thickness is not accounted.

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect to LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.db()

# Result to extract:
entity = "Stress"
component = "SY"
location = "nodal"  # Can be "nodal", "Gauss" / "Internal"

print_decimals = 3  # Number of decimal places to print in the text window
print_in_grid = True  # If True, results are printed in a grid window instead of the text window

# Check if a line is selected
if lusas.selection().count("Line") == 0:
    raise Exception("No line selected. Please select a line to get results from.")

# Get the first selected line
target_line : 'IFLine' = lusas.selection().getObjects("Line")[0]


#####################################################
# Create a graph inspection line
inspection_line = database.createInspectionLine("Temp_InspLine")

# Set inspection line range
inspection_line.setExtent("Full model")
# Can also be "group" followed by group name
# inspection_line.setExtent("group", group_name)

# You can also set a fixed distance interval (in model units) between points where data are extracted
# if not set, data at the element boundaries will be extracted
#inspection_line.setFixedDistance(data_interval), e.g. 0.1
# Alternatively, you can set the number of locations along the line (evenly spaced), e.g. 100 locations
#inspection_line.setEvenSpacing(100)
# Mind that if no results are found at these locations along the line, the NA value is returned.

# Set search projection direction to global Z direction
inspection_line.setProjection(0, 0, 1.0)

# Define the geometry of the inspection line (based on the selected line)
geom_data = lusas.newGeometryData()
geom_data.setCreateMethod("straight")
geom_data.setLowerOrderGeometryType("coordinates")
p1 = target_line.getStartPoint()
p2 = target_line.getEndPoint()
geom_data.addCoords(p1.getX(False), p1.getY(False), p1.getZ(False), True)
geom_data.addCoords(p2.getX(False), p2.getY(False), p2.getZ(False), True)
inspection_line.setLocationLine(geom_data)


#####################################################
# Create/Get slice
# Get Results Component Sets

# Get the internal point results for all thick beam elements
results_set = database.getResultsComponentSet(entity, component, location)
component_index = results_set.getComponentNumber(component)

# Get slice results
distances, values = results_set.getGraphSliceData(component_index, inspection_line)

# Clean up & free up memory
results_set = None
database.Delete(inspection_line)


#####################################################
# Print slice results

# For NA values, LUSAS returns the following very small number
NA_VALUE = 2.2250738585072014e-308

if print_in_grid:
    # Print results to grid window
    grid : 'IFLPIGridWindow' = lusas.createGridWindow(lusas.nextGridWindowID())
    title = f"Slice results ({entity}, {component}, {location})"
    grid.createTab(title, title)
    grid.setColHeaders(title, ["Distance", "Value"])

    # Create 2D array for grid data
    data = []
    for i in range(len(values)):
        row = [round(distances[i], print_decimals)]
        if values[i] != NA_VALUE:
            row.append(round(values[i], print_decimals))
        else:
            row.append("NA")
        data.append(row)
    
    grid.setData(title, data, False, False, False)

else:
    # Print results to text window
    print("-" * 50)
    print(f"Slice results ({entity}, {component}, {location})")
    print("Distance, Value")

    for i in range(len(values)):
        if values[i] != NA_VALUE:
            print(f"{round(distances[i], print_decimals)}, {round(values[i], print_decimals)}")
        else:
            print(f"{round(distances[i], print_decimals)}, NA")


#####################################################
# Post-process results

# Remove NA values (NA values can be returned from elements without results, i.e. deactivated elements)
filtered_distances = []
filtered_values = []

for i in range(len(values)):
    if values[i] != NA_VALUE:
        filtered_distances.append(distances[i])
        filtered_values.append(values[i])

cnt = len(filtered_distances)

# Compute total resultant (integration using trapezoidal rule) and total moment (moment about centroid of slice)
total_resultant = 0
total_moment = 0

if cnt > 1:
    centroid = (filtered_distances[0] + filtered_distances[cnt - 1]) / 2
else:
    centroid = 0

for i in range(1, cnt):
    d0 = filtered_distances[i - 1]
    d1 = filtered_distances[i]
    v0 = filtered_values[i - 1]
    v1 = filtered_values[i]
    seg_length = abs(d1 - d0)
    avg_value = (v0 + v1) / 2
    total_resultant = total_resultant + avg_value * seg_length
    seg_centroid = (d0 + d1) / 2
    arm = centroid - seg_centroid
    total_moment = total_moment + avg_value * seg_length * arm
thickness = filtered_distances[cnt - 1] - filtered_distances[0]

# Output results
if print_in_grid:
    grid.createTab("Summary", "Summary")
    grid.setColHeaders("Summary", ["Description", "Value"])
    summary_data = [
        ["Slice total resultant", round(total_resultant, print_decimals)],
        ["Slice total moment", round(total_moment, print_decimals)],
        ["Slice thickness", round(thickness, print_decimals)]
    ]
    grid.setData("Summary", summary_data, False, False, False)
else:
    print("-" * 50)
    print(f"Slice total resultant: {round(total_resultant, print_decimals)}")
    print(f"Slice total moment: {round(total_moment, print_decimals)}")
    print(f"Slice thickness: {round(thickness, print_decimals)}")
