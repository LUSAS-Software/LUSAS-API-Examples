' LUSAS API (LPI) EXAMPLES
' (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
'
' Example:      Helpers.vbs
' Description:  This file contains helper functions to create points, lines, surfaces, and volumes in the LUSAS database.
'               Copy and paste these functions into your own scripts.
' 

' This function creates a point from coordinates.
Function create_point(x, y, z)
    Set geom_data = newGeometryData().setLowerOrderGeometryType("coordinates").addCoords(x, y, z)
    Set create_point = database.createPoint(geom_data).getObject("Point")
End Function

' This function creates a point from coordinates.
Function create_line_by_coordinates(x1, y1, z1, x2, y2, z2)
    Set geometry_data = newGeometryData().setLowerOrderGeometryType("coordinates").setCreateMethod("straight").addCoords(x1, y1, z1).addCoords(x2, y2, z2)
    Set create_line_by_coordinates = database.createLine(geometry_data).getObjects("Line")(0)
End Function

' This function creates a line from two points.
Function create_line_from_points(p1, p2)
    Set geom_data = newGeometryData().setCreateMethod("straight").setLowerOrderGeometryType("points")
    Set create_line_from_points = newObjectSet().add(p1).add(p2).createLine(geom_data).getObject("Line")
End Function

' This function creates a line from coordinates.
Function create_surface_by_coordinates(x, y, z)
    Set geometry_data = newGeometryData().setCreateMethod("coons").setLowerOrderGeometryType("coordinates")
    For i = 0 To UBound(x)
        geometry_data.addCoords x(i), y(i), z(i)
    Next
    Set create_surface_by_coordinates = database.createSurface(geometry_data).getObjects("Surface")(0)
End Function

' This function creates a surface from coordinates.
Function create_volume_by_surfaces(surfaces)
    Set geometry_data = newGeometryData().setCreateMethod("solidVolume").setExtractAllVolumes()
    Set create_volume_by_surfaces = newObjectSet().add(surfaces).createVolume(geometry_data).getObjects("Volume")(0)
End Function


' This function sweeps points in the specified direction to create lines.
' (sweep_Ext function is required)
Function sweep_points(points, vector)
    Set myObj = newObjectSet().add(points)
    sweep_points = sweep_Ext(myObj, vector, "Line").getObjects("Lines")
End Function

' This function sweeps lines in the specified direction to create surfaces.
' (sweep_Ext function is required)
Function sweep_lines(lines, vector)
    Set myObj = newObjectSet().add(lines)
    sweep_lines = sweep_Ext(myObj, vector, "Surface").getObjects("Surfaces")
End Function

' This function sweeps surfaces in the specified direction to create volumes.
' (sweep_Ext function is required)
Function sweep_surfaces(surfs, vector)
    Set myObj = newObjectSet().add(surfs)
    sweep_surfaces = sweep_Ext(myObj, vector, "Volume").getObjects("Volumes")
End Function

' This function sweeps the given object set in the specified direction to create a new object set.
' (This function is used internally by the other sweep functions)
Function sweep_Ext(targetObjSet, vector, hofType)
    Dim types, MaximumDimension, attr, geomData, objSet
    types = Array("Point", "Line", "Surface", "Volume")
    MaximumDimension = -1
    For i = 0 To UBound(types)
        If types(i) = hofType Then
            MaximumDimension = i
            Exit For
        End If
    Next
    Set attr = database.createTranslationTransAttr("Temp_SweepTranslation", vector).setSweepType("straight").setHofType(hofType)
    Set geomData = newGeometryData().setMaximumDimension(MaximumDimension).setTransformation(attr).sweptArcType("straight")
    Set sweep_Ext = targetObjSet.sweep(geomData)
    database.deleteAttribute attr
End Function


' This function sweeps points in a rotational manner to create lines.
' (sweep_rotationally_Ext function is required)
Function sweep_points_rotationally(points, degrees, origin, aboutAxis)
    If IsEmpty(origin) Then origin = Array(0, 0, 0)
    If aboutAxis = "" Then aboutAxis = "z"

    Set myObj = newObjectSet().add(points)
    sweep_points_rotationally = sweep_rotationally_Ext(myObj, origin, "Line", degrees, aboutAxis).getObjects("Lines")
End Function

' This function sweeps lines in a rotational manner to create surfaces.
' (sweep_rotationally_Ext function is required)
Function sweep_lines_rotationally(lines, degrees, origin, aboutAxis)
    If IsEmpty(origin) Then origin = Array(0, 0, 0)
    If aboutAxis = "" Then aboutAxis = "z"

    Set myObj = newObjectSet().add(lines)
    sweep_lines_rotationally = sweep_rotationally_Ext(myObj, origin, "Surface", degrees, aboutAxis).getObjects("Surfaces")
End Function

' This function sweeps surfaces in a rotational manner to create volumes.
' (sweep_rotationally_Ext function is required)
Function sweep_surfaces_rotationally(surfs, degrees, origin, aboutAxis)
    If IsEmpty(origin) Then origin = Array(0, 0, 0)
    If aboutAxis = "" Then aboutAxis = "z"

    Set myObj = newObjectSet().add(surfs)
    sweep_surfaces_rotationally = sweep_rotationally_Ext(myObj, origin, "Volume", degrees, aboutAxis).getObjects("Volumes")
End Function

' This function sweeps the given object set in a rotational manner to create a new object set.
' (This function is used internally by the other sweep functions)
Function sweep_rotationally_Ext(targetObjSet, origin, hofType, degree, aboutAxis)
    types = Array("Point", "Line", "Surface", "Volume")
    For i = 0 To UBound(types)
        If types(i) = hofType Then
            MaximumDimension = i
            Exit For
        End If
    Next
    If aboutAxis = "" Then aboutAxis = "z"

    title = "Temp_SweepRotation"
    If LCase(aboutAxis) = "x" Then
        Set attr = database.createYZRotationTransAttr(title, degree, origin)
    ElseIf LCase(aboutAxis) = "y" Then
        Set attr = database.createXZRotationTransAttr(title, degree, origin)
    Else
        Set attr = database.createXYRotationTransAttr(title, degree, origin)
    End If
    attr.setSweepType("minorArc").setHofType(hofType)

    Set geomData = newGeometryData().setMaximumDimension(MaximumDimension).setTransformation(attr).sweptArcType("minorArc")

    Set sweep_rotationally_Ext = targetObjSet.sweep(geomData)
    database.deleteAttribute attr
End Function


' This function deletes all contents of the database.
Sub delete_all_database_contents(db)
    database.closeAllResults()
    database.deleteLoadsets "Envelopes"
    database.deleteLoadsets "Smart Combinations"
    database.deleteLoadsets "Basic Combinations"
    database.deleteAllAnalyses()
    database.deleteAllNoGroups()
    database.deleteAllAttributes()
    database.deleteAllUtilities()
    database.deleteAll()
    database.createAnalysisStructural "Analysis 1"
End Sub


' This function creates reinforcing bar attributes in the LUSAS database.
Function create_reinforcing_bar_attributes(db, diameters)
    Dim names(), i, dia, name, util, attr
    ReDim names(UBound(diameters))

    For i = 0 To UBound(diameters)
        dia = diameters(i)
        name = "Bar " & dia

        Set util = db.createParametricSection(name)
        util.setType "Circular Solid"
        util.setDimensions Array("D"), Array(dia)

        Set attr = db.createGeometricLine(name)
        attr.setFromLibrary "Utilities", "", name, 0, 0, 0

        names(i) = name
    Next

    create_reinforcing_bar_attributes = names
End Function


' This function creates a circular section in the LUSAS database.
Function create_circular_section(db, name, dia)
    Dim util, attr
    Set util = database.createParametricSection(name)
    util.setType "Circular Solid"
    util.setDimensions Array("D"), Array(dia)

    Set attr = database.createGeometricLine(name)
    attr.setFromLibrary "Utilities", "", name, 0, 0, 0

    Set create_circular_section = attr
End Function

' This function creates a rectangular section in the LUSAS database.
Function create_rectangular_section(db, name, breadth, depth)
    Dim util, attr
    Set util = database.createParametricSection(name)
    util.setType "Rectangular Solid"
    util.setDimensions Array("B", "D"), Array(breadth, depth)

    Set attr = database.createGeometricLine(name)
    attr.setFromLibrary "Utilities", "", name, 0, 0, 0

    Set create_rectangular_section = attr
End Function
