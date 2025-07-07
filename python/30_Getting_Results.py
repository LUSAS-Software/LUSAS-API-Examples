# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      30_Getting_Results.py
# Description:  Extract nodal and element results from the running LUSAS model.
#               This example does the extraction in different approaches. It is recommended to use the results component set approach for most cases.
#               To compare the different approaches, it is recommended that the Jupyter Notebook example is used instead.
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *
# Time module to measure execution time
import time

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# To successfully run the code below you must have a model solved (e.g. the model generated from example 15).
# Throw error if no model is open:
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.db()

# Get selected items and add related Elements and Nodes
target = lusas.newObjectSet().add(lusas.selection()).addLOF("Element").addLOF("Node")
targetNodes : list[IFNode] = lusas.selection().getObjects("Node")
targetElements : list[IFElement] = target.getObjects("Element")

if len(targetNodes) == 0:
    raise Exception("No features selected. Please select some nodes/elements to get results from.")

# To successfully run the code below you must have a model solved.


######################################################
## Nodal Results
# All nodes have displacement results. Here we simply loop through the nodes contained in the current selection and ask for the results of displacement and printing them
start = time.time()

# Print displacements (model units)
print("Displacement results:")
for n in targetNodes:
    dx = n.getResults("Displacement", "DX")
    dy = n.getResults("Displacement", "DY")
    dz = n.getResults("Displacement", "DZ")
    print(dx, dy, dz)
print(f"Execution time for displacement results: {time.time() - start} seconds")

# Print reactions and calculate total reactions (model units)
start = time.time()
total_fx, total_fy, total_fz = 0, 0, 0
print("Reaction results:")
for n in targetNodes:
    # Non supported nodes will return a value of 2.2250738585072014e-308.
    # This is the smallest possible value represented by a 64bit double precision variable.
    # This value is equivalent to N/A.
    # This can also be checked using the Helpers.isNan() function.
    fx = n.getResults("Reaction", "FX")
    if fx == 2.2250738585072014e-308:
        fx = 0
    fy = n.getResults("Reaction", "FY")
    if fy == 2.2250738585072014e-308:
        fy = 0
    fz = n.getResults("Reaction", "FZ")
    if fz == 2.2250738585072014e-308:
        fz = 0
    print(fx, fy, fz)

    total_fx += fx
    total_fy += fy
    total_fz += fz

# Print total reactions (model units)
print(f"Total reactions of selected nodes : {fx:.2f}, {fy:.2f}, {fz:.2f}")
print(f"Execution time for reaction results: {time.time() - start} seconds")

# NOTE:
# The getResults function has 3 additional optional arguments as shown in the LPI Reference manual
# `getResults(entity, component, [units], [loadcase], [context])`
# 
# The results we have been getting so far have been in model units and for the active loadset. 
# The first additional argument allows us to ask for results in a different unit set.
# The second additional argument is actually a return value that is used when the active loadset is an envelope. In this case the loadcase causing the requested results is returned through this argument.
# The third argument allows us to specify other settings for the results such as a different loadset. We will return to resultsets later.


######################################################
## Element Results

# Elements do not have a getResults() function like nodes because elements have many different types of results. Shells beams, solids and joint elements all have different results and result locations.
# 
# A beam element for example has results at each node, it also has a series of intermediate or "internal" results.
# A shell element also nodal results at each node but it does not have internal results, instead it has additional results at the gauss/integration points 
# 
# The element interface therefore has several functions to deal with these differences and its up to you to call the correct one for the element you are looking at.
# 
# If we ask the database for all elements, that's exactly what we'll get and we'd have to write a lot of code to handle the various element types as follows:
start = time.time()

print("Force/Moment results: (from beam elements)")
for e in targetElements:
    stressType = e.getStressType()
    if e.getDomainDimension() == 1: # Beam Element
        if stressType == "Thick 3D Beam":
            # Get bending moment My for each internal point
            for i in range(0, e.countInternalPoints()):
                my = e.getInternalResults(i, "Force/Moment - Thick 3D Beam", "My")
                print(my)
            # Or get the internal results as an array
            my = e.getInternalResultsArray("Force/Moment - Thick 3D Beam", "My")

    elif e.getDomainDimension() == 2: # Shell Element
        pass

    elif e.getDomainDimension() == 3: # Solid Element
        pass
print(f"Execution time for Force/Moment results (from beam elements): {time.time() - start} seconds")

# The above can be repeated for all element types but you may have noticed that this approach is very slow and not recommended.
# A much better approach is to use results component sets.


######################################################
## Results Component Sets
# A results component set is a container for a particular set of results. It is much more efficient than asking for results all at once.
start = time.time()

# Get the internal point results for all thick beam elements
results_my = lusas.database().getResultsComponentSet("Force/Moment - Thick 3D Beam", "My", "Internal")
i_my = results_my.getComponentNumber("My")

print("Force/Moment results: (from beam elements using ResultsComponentSet)")
for e in targetElements:
    stressType = e.getStressType()
    if e.getDomainDimension() == 1: # Beam Element
        if stressType == "Thick 3D Beam":
            # Note the unitset is not optional but providing None uses the current database units
            my = results_my.getInternalResultsArray(i_my, e, None)
            print(my)
print(f"Execution time for Force/Moment results (from beam elements using ResultsComponentSet): {time.time() - start} seconds")



## Instead of checking all elements and their type, we can filter them using an Object Set.
# Depending on what your model contains the following code should run much quicker than previous methods. This is because we filtered out only the elements of interest and removed any subsequent type checking.
start = time.time()

# Create an object set containing only the thick 3d beam elements.
beamsObjSet = lusas.newObjectSet().add(targetElements).keep("Thick 3D Beam")

# Get the internal point results for all thick beam elements
print("Force/Moment results: (from ObjectSet using ResultsComponentSet)")
for e in beamsObjSet.getObjects("Element"):
    # Note the unitset is not optional but providing None uses the current database units
    my = results_my.getInternalResultsArray(i_my, e, None)
    print(my)
print(f"Execution time for Force/Moment results (from ObjectSet using ResultsComponentSet): {time.time() - start} seconds")

# Remember clear the results component set if not used again to free up memory (commented in this case since we are using it again)
#results_my = None 


## The final piece of the puzzle is to provide a results context.
# Results context can be set to any loadcase and set of elements so we are no longer relying on the active settings of the user interface.
start = time.time()

# Create a results context for the beam elements
context = lusas.newResultsContext(None)
# Set target elements
context.getCalcResultsSet().add(beamsObjSet)
# Set loadset 1 as the active loadset of the context
context.setActiveLoadset(1)

print("Force/Moment results: (from ObjectSet using ResultsComponentSet and set context)")
for e in beamsObjSet.getObjects("Element"):
    # Note the unitset is not optional but providing None uses the current database units
    my = results_my.getInternalResultsArray(i_my, e, None)
    print(my)
print(f"Execution time for Force/Moment results (from ObjectSet using ResultsComponentSet and set context): {time.time() - start} seconds")

# Free up memory if the script will continue to run (not required in this case
results_my = None
context = None
beamsObjSet = None


# The general principle laid out above can be used for all elements, nodes and inspection location results.
