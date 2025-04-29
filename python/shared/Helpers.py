from shared.LPI_21_1 import *

def initialise(modeller:'IFModeller'):
    global lusas
    lusas = modeller

def create_point(x:float, y:float, z:float) -> 'IFPoint':
    """Helper function to create a point from coordinates

    Args:
        x (float): Global X coordinate
        y (float): Global Y coordinate
        z (float): Global Z coordinate

    Returns:
        IFPoint: Point in the IFDatabase
    """    
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults() 
    # set the options for creating points from coordinates
    geom_data.setLowerOrderGeometryType("coordinates")
    # Add the coordinates
    geom_data.addCoords(x, y, z)
    # Create the point and return it. 
    # Note that createPoint returns and IFObjectSet from which we can get the point.
    return win32.CastTo(lusas.database().createPoint(geom_data).getObject("Point"), "IFPoint")

def create_line_by_coordinates(x1:float, y1:float, z1:float, x2:float, y2:float, z2:float,) -> 'IFLine':
    """Helper function to create a line from coordinates

    Args:
        x1 (float): Starting point global X coordinate
        y1 (float): Starting point global Y coordinate
        z1 (float): Starting point global Z coordinate
        x2 (float): Ending point global X coordinate
        y2 (float): Ending point global Y coordinate
        z2 (float): Ending point global Z coordinate

    Returns:
        IFLine: Line in the IFDatabase
    """

    geometry_data = lusas.geometryData().setAllDefaults()
    geometry_data.setLowerOrderGeometryType("coordinates")
    geometry_data.setCreateMethod("straight")
    geometry_data.addCoords(x1, y1, z1)
    geometry_data.addCoords(x2, y2, z2)
    newLine:IFLine = lusas.database().createLine(geometry_data).getObjects("Line")[0]
    return newLine

def create_line_from_points(p1:'IFPoint', p2:'IFPoint') -> 'IFLine':
    """Helper function to create a line from two point objects.

    Args:
        p1 (IFPoint): Start point
        p2 (IFPoint): End point

    Returns:
        IFLine: Straight line connecting the two points
    """    
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults()         
    # set the options for creating straight lines from points
    geom_data.setCreateMethod("straight").setLowerOrderGeometryType("points")        
    # Create an object set to contain the points and use this set to create the line
    obs = lusas.newObjectSet()                 
    obs.add(p1)
    obs.add(p2)
    # Create the line, get the line object array from the returned object set
    return win32.CastTo(obs.createLine(geom_data).getObject("Line"), "IFLine")

def create_line(p1:list[float], p2:list[float]) -> 'IFLine':
    """Helper function to create a straight line from two point coordinates defined 

    Args:
        p1 (list[float]): List of 3 floats x,y,z
        p2 (list[float]): List of 3 floats x,y,z

    Returns:
        IFLine: Straight line between the two point coordinates
    """
    assert len(p1) == len(p2) == 3, "Point coordinates must be a list of 3 values (x,y,z)"
    # geometryData object contains all the settings to perform a geometry creation
    geom_data = lusas.geometryData().setAllDefaults()  
    # Set the options for creating straight lines from coordinates
    geom_data.setCreateMethod("straight")        
    geom_data.setLowerOrderGeometryType("coordinates")        
    
    # Add the coordinates, lines directions will follow the order of the coordinates
    geom_data.addCoords(p1[0], p1[1], p1[2])    # Set the coordinates of the first point X,Y,Z
    geom_data.addCoords(p2[0], p2[1], p2[2])    # Set the coordinates of the second point X,Y,Z

    # Create the line, get the line objects from the returned object set
    return win32.CastTo(lusas.database().createLine(geom_data).getObject("Line"), "IFLine")

def create_surface_by_coordinates(x:list[float], y:list[float], z:list[float]) -> IFSurface:
    """Helper function to create a surface from coordinates

    Args:
        x (list): List of X coordinates
        y (list): List of Y coordinates
        z (list): List of Z coordinates

    Returns:
        IFSurface: Surface in the IFDatabase
    """
    geometry_data = lusas.newGeometryData()
    geometry_data.setCreateMethod("coons")
    geometry_data.setLowerOrderGeometryType("coordinates")
    for i in range(len(x)):
        geometry_data.addCoords(x[i], y[i], z[i])
    surf : IFSurface = lusas.db().createSurface(geometry_data).getObjects("Surface")[0]
    return surf

def create_volume_by_surfaces(surfaces:list[IFSurface]) -> IFVolume:
    """Helper function to create a volume from surfaces

    Args:
        surfaces (list): List of surfaces

    Returns:
        IFVolume: Volume in the IFDatabase
    """
    # Create a geometryData object to contain all the settings for the geometry creation
    geometry_data = lusas.newGeometryData()
    # Set the options for creating geometries from surfaces
    geometry_data.setCreateMethod("solidVolume")
    geometry_data.setExtractAllVolumes()
    # create an object set to contain the surfaces and use this set to create the volume
    surfsObj = lusas.newObjectSet().add(surfaces)
    # Create the volume using the surfaces
    vlm : IFVolume = surfsObj.createVolume(geometry_data).getObjects("Volume")[0]
    return vlm

def sweep_points(pnts:list[IFPoint], vector: list[float]) -> list[IFLine]:
    """
    Sweeps the given points in the specified direction to create lines.

    Args:
        pnts (list): List of points to be swept
        vector (list): Direction vector for the sweep

    Returns:
        list: List of lines created by sweeping the points
    """
    try:
        myObj = lusas.newObjectSet().add(pnts)
        lines : list[IFLine] = sweep_Ext(myObj, vector, "Line").getObjects("Lines")
    except Exception as e:
        print(f"Error sweeping points: {str(e)}")
        return []
    return lines

def sweep_lines(lines:list[IFLine], vector: list[float]) -> list[IFSurface]:
    """
    Sweeps the given lines in the specified direction to create surfaces.

    Args:
        lines (list): List of lines to be swept
        vector (list): Direction vector for the sweep

    Returns:
        list: List of surfaces created by sweeping the lines
    """
    try:
        myObj = lusas.newObjectSet().add(lines)
        surfs : list[IFSurface] = sweep_Ext(myObj, vector, "Surface").getObjects("Surfaces")
    except Exception as e:
        print(f"Error sweeping lines: {str(e)}")
        return []
    return surfs

def sweep_surfaces(surfs:list[IFSurface], vector: list[float]) -> list[IFVolume]:
    """
    Sweeps the given surfaces in the specified direction to create volumes.

    Args:
        surfs (list): List of surfaces to be swept
        vector (list): Direction vector for the sweep

    Returns:
        list: List of volumes created by sweeping the surfaces
    """
    try:
        myObj = lusas.newObjectSet().add(surfs)
        vlms : list[IFVolume] = sweep_Ext(myObj, vector, "Volume").getObjects("Volumes")
    except Exception as e:
        print(f"Error sweeping surfaces: {str(e)}")
        return []
    return vlms

def sweep_Ext(trgtObjSet:IFObjectSet, vector: list[float], hofType:str):
    """
    Sweeps the given object set in the specified direction to create a new object set.

    Args:
        trgtObjSet (IFObjectSet): The object set to be swept
        vector (list): Direction vector for the sweep
        hofType (str): Type of the object to be created ("Point", "Line", "Surface", "Volume")

    Returns:
        IFObjectSet: The new object set created by sweeping the original object set
    """
    types = ["Point", "Line", "Surface", "Volume"]
    MaximumDimension = types.index(hofType)

    attr = lusas.db().createTranslationTransAttr("Temp_SweepTranslation", vector)
    attr.setSweepType("straight")
    attr.setHofType(hofType)

    geomData = lusas.newGeometryData()
    geomData.setMaximumDimension(MaximumDimension)
    geomData.setTransformation(attr)
    geomData.sweptArcType("straight")

    objSet = trgtObjSet.sweep(geomData)
    lusas.db().deleteAttribute(attr)

    return objSet

def sweep_points_rotationally(pnts:list[IFPoint], degrees : float, origin: list[float] = [0, 0, 0], aboutAxis : str = "z") -> list[IFLine]:
    """
    Sweeps the given points in the specified degrees to create lines.
    
    Args:
        pnts (list): List of points to be swept
        degrees (float): Degrees for the sweep
        origin (list): Origin point for the sweep
        aboutAxis (str): Axis of rotation ("x", "y", "z")

    Returns:
        list: List of lines created by sweeping the points
    """
    try:
        myObj = lusas.newObjectSet().add(pnts)
        lines : list[IFLine] = sweep_rotationally_Ext(myObj, origin, "Line", degrees, aboutAxis).getObjects("Lines")
    except Exception as e:
        print(f"Error sweeping points: {str(e)}")
        return []
    return lines

def sweep_lines_rotationally(lines:list[IFLine], degrees : float, origin: list[float] = [0, 0, 0], aboutAxis : str = "z") -> list[IFSurface]:
    """
    Sweeps the given lines in the specified degrees to create surfaces.

    Args:
        lines (list): List of lines to be swept
        degrees (float): Degrees for the sweep
        origin (list): Origin point for the sweep
        aboutAxis (str): Axis of rotation ("x", "y", "z")

    Returns:
        list: List of surfaces created by sweeping the lines
    """
    try:
        myObj = lusas.newObjectSet().add(lines)
        surfs : list[IFSurface] = sweep_rotationally_Ext(myObj, origin, "Surface", degrees, aboutAxis).getObjects("Surfaces")
    except Exception as e:
        print(f"Error sweeping lines: {str(e)}")
        return []
    return surfs

def sweep_surfaces_rotationally(surfs:list[IFSurface], degrees : float, origin: list[float] = [0, 0, 0], aboutAxis : str = "z") -> list[IFVolume]:
    """
    Sweeps the given surfaces in the specified degrees to create volumes.

    Args:
        surfs (list): List of surfaces to be swept
        degrees (float): Degrees for the sweep
        origin (list): Origin point for the sweep
        aboutAxis (str): Axis of rotation ("x", "y", "z")

    Returns:
        list: List of volumes created by sweeping the surfaces
    """
    try:
        myObj = lusas.newObjectSet().add(surfs)
        vlms : list[IFVolume] = sweep_rotationally_Ext(myObj, origin, "Volume", degrees, aboutAxis).getObjects("Volumes")
    except Exception as e:
        print(f"Error sweeping surfaces: {str(e)}")
        return []
    return vlms

def sweep_rotationally_Ext(trgtObjSet:IFObjectSet, origin:list, hofType:str, degree:float, aboutAxis:str=None):
    """
    Sweeps the given object set in a rotational manner to create a new object set.

    Args:
        trgtObjSet (IFObjectSet): The object set to be swept
        origin (list): Origin point for the sweep
        hofType (str): Type of the object to be created ("Point", "Line", "Surface", "Volume")
        degree (float): Degrees for the sweep
        aboutAxis (str): Axis of rotation ("x", "y", "z")

    Returns:
        IFObjectSet: The new object set created by sweeping the original object set
    """
    types = ["Point", "Line", "Surface", "Volume"]
    MaximumDimension = types.index(hofType)

    if aboutAxis is None:
        aboutAxis = "z"

    title = "Temp_SweepRotation"
    if aboutAxis.lower() == "x":
        attr = lusas.db().createYZRotationTransAttr(title, degree, origin)
    elif aboutAxis.lower() == "y":
        attr = lusas.db().createXZRotationTransAttr(title, degree, origin)
    else:
        attr = lusas.db().createXYRotationTransAttr(title, degree, origin)

    attr.setSweepType("minorArc")
    attr.setHofType(hofType)

    geomData = lusas.newGeometryData()
    geomData.setMaximumDimension(MaximumDimension)
    geomData.setTransformation(attr)
    geomData.sweptArcType("minorArc")

    objSet = trgtObjSet.sweep(geomData)
    lusas.db().deleteAttribute(attr)

    return objSet


def delete_all_database_contents(db:'IFDatabase'):
    """Delete all contents of the database

    Parameters:
        db (IFDatabase): Reference to the database
    """
    # Close any previous results
    db.closeAllResults()

    # Delete all previous model data
    db.deleteLoadsets("Envelopes")
    db.deleteLoadsets("Smart Combinations")
    db.deleteLoadsets("Basic Combinations")
    db.deleteAllAnalyses()
    db.deleteAllNoGroups()
    db.deleteAllAttributes()
    db.deleteAllUtilities()
    db.deleteAll()

    db.createAnalysisStructural("Analysis 1")

def get_Analysis_Loadcases(analysis : IFAnalysis) -> list[IFLoadcase]:
    """
    Get all loadcases of an analysis. In v22.0, this can be acquired directly from the analysis object as analysis.getLoadcases().

    Args:
        analysis (IFAnalysis): Analysis object

    Returns:
        list[IFLoadcase]: List of loadcases in the analysis
    """
    analysisName = analysis.getName()
    allLoadcases : list['IFLoadcase'] = lusas.db().getLoadsets("Loadcase")
    loadcases : list['IFLoadcase'] = list(filter(lambda lc: lc.getAnalysis().getName() == analysisName, allLoadcases))
    return loadcases

def create_reinforcing_bar_attributes(db:'IFDatabase', diameters:list) -> list:
    """Create geometric attributes representing individual bars in the LUSAS Database

    Args:
        db (IFDatabase): Reference to the database
        diameters (list): List of diameters for which geometric attributes will be created

    Returns:
        list: Names of the created attributes in the form 'Bar <diameter>'
    """    
    names = []
    for dia in diameters:
        name = f"Bar {dia}"
        util = db.createParametricSection(name)
        util.setType("Circular Solid")
        util.setDimensions(['D'], [dia])

        attr = db.createGeometricLine(name)
        attr.setFromLibrary("Utilities", "", name, 0, 0, 0)
        names.append(name)
    return names



def create_circular_section(db:'IFDatabase', name:str, dia:float) -> 'IFGeometricLine':
    """Creates a geometric attribute based on a parametric circular definition

    Args:
        db (IFDatabase): Reference to the database
        name (str): Name of the attribute to be created
        dia (float): Diameter

    Returns:
        IFGeometricLine: Reference to the created geometric attribute
    """    
    util = db.createParametricSection(name).setType("Circular Solid").setDimensions(['D'], [dia])
    return db.createGeometricLine(name).setFromLibrary("Utilities", "", name, 0, 0, 0)


def create_rectangular_section(db:'IFDatabase', name:str, breadth:float, depth:float) -> 'IFGeometricLine':
    """Creates a geometric attribute based on a parametric rectandular definition

    Args:
        db (IFDatabase): Reference to the database
        name (str): Name of the attribute to be created
        breadth (float): Breadth of the section
        depth (float): Depth of the section

    Returns:
        IFGeometricLine: Reference to the created geometric attribute
    """    
    util = db.createParametricSection(name).setType("Rectangular Solid")
    util.setDimensions(['B', 'D'], [breadth, depth])

    return db.createGeometricLine(name).setFromLibrary("Utilities", "", name, 0, 0, 0)
    
def get_loadcase(db:IFDatabase, id:int) -> IFLoadcase:
    """Get a loadcase from the database by its ID

    Args:
        db (IFDatabase): Reference to the database
        id (int): ID of the loadcase

    Returns:
        IFLoadcase: Loadcase object
    """
    loadset = db.getLoadset(id)
    return win32.CastTo(loadset, "IFLoadcase")