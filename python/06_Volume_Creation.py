# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      06_Volume_Creation.py
# Description:  Creates volumes in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

# Throw error if no model is open
# alternatively, you can use `lusas.newProject("Structural")` to create a new model
if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")

# Save database in variable
database = lusas.database()


######################################################
### Create a Volumes from Surfaces

# Create a list of surfaces to be used in the volume creation
import shared.Helpers as Helpers
Helpers.initialise(lusas)
surfaces = [
    Helpers.create_surface_by_coordinates([0,1,1,0], [0,0,1,1], [0,0,0,0]), #Bottom Surface (z=0)
    Helpers.create_surface_by_coordinates([0,1,1,0], [0,0,1,1], [1,1,1,1]), #Top Surface (z=1)
    Helpers.create_surface_by_coordinates([0,1,1,0], [0,0,0,0], [0,0,1,1]), #Front Surface (y=0)
    Helpers.create_surface_by_coordinates([0,1,1,0], [1,1,1,1], [0,0,1,1]), #Back Surface (y=1)
    Helpers.create_surface_by_coordinates([0,0,0,0], [0,1,1,0], [0,0,1,1]), #Left Surface (x=0)
    Helpers.create_surface_by_coordinates([1,1,1,1], [0,1,1,0], [0,0,1,1]), #Right Surface (x=1)
]

# Create a geometryData object to contain all the settings for the geometry creation
geom_data = lusas.newGeometryData()
# set the options for creating geometries from surfaces
geom_data.setCreateMethod("solidVolume")
geom_data.setExtractAllVolumes()

# create an object set to contain the surfaces and use this set to create the volume
surfsObj = lusas.newObjectSet()
surfsObj.add(surfaces)

# Create the volume using the surfaces
vlm : IFVolume = database.createVolume(geom_data).getObjects("Volume")[0]
print(f"Volume {vlm.getID()} created by surfaces.")


######################################################
### Volume from Surface translational sweep

# Create a surface to be used in the volume creation
surface = surfaces[0] # Bottom Surface

# Sweep vector x, y, z
vector = [0, 0, -1]

# Create a translation attribute
attr = database.createTranslationTransAttr("Temp_SweepTranslation", vector)
attr.setSweepType("straight")
attr.setHofType("Volume") # Set target geometry

geomData = lusas.newGeometryData()
geomData.setMaximumDimension(3) # Target geometries (0: Points, 1: Lines, 2: Surfaces)
geomData.setTransformation(attr)
geomData.sweptArcType("straight")

# Create an object set to contain the points and be swept
obs = lusas.newObjectSet().add(surface)

# Perform the sweep, the returned object set will contain the created surfaces
objSet = obs.sweep(geomData)

# Delete the translation attribute
database.deleteAttribute(attr)

# Print new line IDs
newVolumes : list[IFVolume] = objSet.getObjects("Volume")
for volume in newVolumes:
    print(f"Volume {volume.getID()} created by sweep.")


######################################################
### Using Helper function
# The Helper module contains some useful functions to simplify the geometry creation process.

# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)

# Surface creation by coordinates:
xs = [1.0, 2, 2, 1]
ys = [0.0, 0, 1, 1]
zs = [0.0, 0, 0, 0]
surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)
print(f"Surface {surface1.getID()} created by coordinates (using helpers).")

# Volume creation by sweeps:
volumes1 = Helpers.sweep_surfaces([surface1], [0, 0, -1])
for volume in volumes1:
    print(f"Volume {volume.getID()} created by sweep (using helpers).")

volumes2 = Helpers.sweep_surfaces_rotationally([surface1], -90, [1, 0, 0], "y") # 45 degrees
for volume in volumes2:
    print(f"Volume {volume.getID()} created by rotational sweep (using helpers).")

# Fit view
lusas.view().setScaledToFit(True)