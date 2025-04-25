# LUSAS API (LPI) PYTHON EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      02d_Volume_Creation.py
# Description:  Creates volumes in the running LUSAS model
# 

# Libraries:
# LUSAS LPI module (easier connection and autocomplete)
from shared.LPI_21_1 import *

# Connect on LUSAS and check if a model is open
lusas = get_lusas_modeller()

if not lusas.existsDatabase():
    raise Exception("A model must be open before running this code")


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
vlm : IFVolume = lusas.db().createVolume(geom_data).getObjects("Volume")[0]


######################################################
### Volume from Surface translational sweep

# Create a surface to be used in the volume creation
surface = surfaces[0] # Bottom Surface

# Sweep vector x, y, z
vector = [0, 0, -1]

# Create a translation attribute
attr = lusas.db().createTranslationTransAttr("Temp_SweepTranslation", vector)
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
lusas.db().deleteAttribute(attr)

# Print new line IDs
newVolumes : list[IFVolume] = objSet.getObjects("Volume")
for volume in newVolumes:
    print(f"Volume {volume.getID()} created from sweep.")


######################################################
### Using Helper function
# The Helper module contains some useful functions to simplify the geometry creation process.

# Import and initialise the Helpers module
import shared.Helpers as Helpers
Helpers.initialise(lusas)

# Surface creation by coordinates:
xs = [0, 1, 1, 0]
ys = [0, 0, 1, 1]
zs = [-4, -4, -4, -4]
surface1 = Helpers.create_surface_by_coordinates(xs, ys, zs)

# Volume creation by sweeps:
volume1 = Helpers.sweep_surfaces([surface1], [0, 0, 1])
volume2 = Helpers.sweep_surfaces_rotationally([surface1], 45) # 45 degrees
