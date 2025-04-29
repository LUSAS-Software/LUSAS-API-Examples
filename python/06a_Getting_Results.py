# LUSAS API (LPI) PYTHON EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      06a_Getting_Results.py
# Description:  Extract nodal and element results from the running LUSAS model.
#               This example does the extraction in different approaches. It is recommended to use the results component set approach for most cases.
#               To compare the different approaches, it is recommended that the Jupyter Notebook example is used instead.
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.db()

# To successfully run the code below you must have a model solved.

# Get selected nodes
selectedNodes : list[IFNode] = lusas.selection().getObjects("Node")

if len(selectedNodes) == 0:
    raise Exception("No nodes selected. Please select some nodes to get results from.")


######################################################
## Nodal Results
# All nodes have displacement results. Here we simply loop through the nodes contained in the current selection and ask for the results of displacement and printing them

# Print displacements (model units)
for n in selectedNodes:
    dx = n.getResults("Displacement", "DX")[0]
    dy = n.getResults("Displacement", "DY")[0]
    dz = n.getResults("Displacement", "DZ")[0]
    print(dx, dy, dz)

# Print reactions and calculate total reactions (model units)
total_fx, total_fy, total_fz = 0, 0, 0
for n in selectedNodes:
    # Non supported nodes will return a value of 2.2250738585072014e-308. This is the smallest possible value represented by a 64bit double precision variable.
    # We can avoid this small value by asking if a result is available
    fx = n.getResults("Reaction", "FX")[0] if n.hasResults("Reaction", "FX") else 0
    fy = n.getResults("Reaction", "FY")[0] if n.hasResults("Reaction", "FY") else 0
    fz = n.getResults("Reaction", "FZ")[0] if n.hasResults("Reaction", "FZ") else 0
    print(fx, fy, fz)

    total_fx += fx
    total_fy += fy
    total_fz += fz

# Print total reactions (model units)
print(f"Total reactions of selected nodes : {fx:.2f}, {fy:.2f}, {fz:.2f}")

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

allElements : list[IFElement] = database.getObjects("Element")
for e in allElements:
    stressType = e.getStressType()
    if e.getDomainDimension() == 1: # Beam Element
        if stressType == "Thick 3D Beam":
            # Get bending moment My for each internal point
            for i in range(0, e.countInternalPoints()):
                my = e.getInternalResults(i, "Force/Moment - Thick 3D Beam", "My")[0]
                print(my)
            # Or get the internal results as an array
            my = e.getInternalResultsArray("Force/Moment - Thick 3D Beam", "My")

    elif e.getDomainDimension() == 2: # Shell Element
        pass

    elif e.getDomainDimension() == 3: # Solid Element
        pass

# The above can be repeated for all element types but you may have noticed that this approach is very slow and not recommended.
# A much better approach is to use results component sets.


######################################################
## Results Component Sets
# A results component set is a container for a particular set of results. It is much more efficient than asking for results all at once.


# Get the internal point results for all thick beam elements
results_my = lusas.database().getResultsComponentSet("Force/Moment - Thick 3D Beam", "My", "Internal")
i_my = results_my.getComponentNumber("My")

for e in allElements:
    stressType = e.getStressType()
    if e.getDomainDimension() == 1: # Beam Element
        if stressType == "Thick 3D Beam":
            # Note the unitset is not optional but providing None uses the current database units
            my = results_my.getInternalResultsArray(i_my, e, None)
            print(my)



## Instead of checking all elements and their type, we can filter them using an Object Set.
# Depending on what your model contains the following code should run much quicker than previous methods. This is because we filtered out only the elements of interest and removed any subsequent type checking.

# Create an object set containing only the thick 3d beam elements.
beams = lusas.newObjectSet().add("Thick 3D Beam")

# Get the internal point results for all thick beam elements
for e in beams.getObjects("Element"):
    # Note the unitset is not optional but providing None uses the current database units
    my = results_my.getInternalResultsArray(i_my, e, None)
    print(my)

# Remember clear the results component set if not used again to free up memory (commented in this case since we are using it again)
#results_my = None 


## The final piece of the puzzle is to provide a results context.
# Results context can be set to any loadcase and set of elements so we are no longer relying on the active settings of the user interface.

# Create a results context for the beam elements
context = lusas.newResultsContext(None)
# Set target elements
context.getCalcResultsSet().add(beams)
# Set loadset 1 as the active loadset of the context
context.setActiveLoadset(1)

for e in beams.getObjects("Element"):
    # Note the unitset is not optional but providing None uses the current database units
    my = results_my.getInternalResultsArray(i_my, e, None)
    print(my)

# Free up memory if the script will continue to run (not required in this case
results_my = None
context = None
beams = None


# The general principle laid out above can be used for all elements, nodes and inspection location results.
