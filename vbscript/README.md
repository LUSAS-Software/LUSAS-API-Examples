# VBScript Examples

Visual Basic Script (VBScript) code (files with *.vb or *.lvb extensions) can be executed within LUSAS through the Main Menu shortcut "Run Script" (red folder icon). One line VBScript commands can also be executed through LUSAS's command bar (by default is set to VBScript). To enable the command bar, navigate to View > LPI Command Bar.

## 📚 Examples Included

| Category   | Description                           | Language   | File                     |
| ---------- | ------------------------------------- | ---------- | ------------------------ |
| General    | Create new model                      | VBScript   | 01a_Create_New_Model.lvb |
| Geometry   | Creates points                        | VBScript   | 02a_Point_Creation.lvb   |
| Geometry   | Creates lines                         | VBScript   | 02b_Line_Creation.lvb    |
| Geometry   | Creates surfaces                      | VBScript   | 02c_Surface_Creation.lvb |
| Geometry   | Creates volumes                       | VBScript   | 02d_Volume_Creation.lvb  |
| Geometry   | Use ObjectSets (Database, Groups, Selection etc) and filter geometries | VBScript   | 03_Get_Geometries_Groups_Selection_ObjectSets.lvb |
| Attributes | Create/assign meshes                  | VBScript   | 04a_Create_and_assign_mesh.lvb     |
| Attributes | Create/assign sections                | VBScript   | 04b_Create_and_assign_section.lvb  |
| Attributes | Create/assign materials               | VBScript   | 04c_Create_and_assign_material.lvb |
| Attributes | Create/assign supports                | VBScript   | 04d_Create_and_assign_supports.lvb |
| Attributes | Create/assign loads                   | VBScript   | 04d_Create_and_assign_loads.lvb    |
| Attributes | Prints the attribute type(s) for the user given attribute names | VBScript   | 04f_Get_attribute_type_by_name.lvb |
| Attributes | Extracts all attributes' properties in a data grid for the user given attribute names | VBScript   | 04g_Extract_attribute_values.lvb |
| Analyses   | Create/solve analyses and loadcases   | VBScript   | 05a_Create_and_Run_Analyses_and_Loadcases.lvb |
| Analyses   | Create Combinations and Envelopes     | VBScript   | 05b_Create_Combinations_and_Envelopes.lvb |
| Analyses   | Create Coupled Structural-Thermal Analysis | VBScript   | 05c_Coupled_Structural_Thermal_Analysis.lvb |
| Results    | Get results from Elements/Nodes            | VBScript   | 06a_Getting_Results.lvb     |
| Results    | Get results with Print Results Wizard      | VBScript   | 06b_Getting_Results_PRW.lvb |

## Code

Scripts should always start with the `$ENGINE=VBScript` command. Since VBScript is executed internally, the code has direct access to all IFModeller methods some of which are listed bellow:

- `database()` or `db()`

- `selection()`

- `view()`

- `visible()`

- `newObjectSet()`

- `geometryData()` and `newGeometryData()`

- `textWin.writeLine()`

Since VBScript does not natively support imports, the following command can be used at the top of `*.lvb` files to import other scripts:
```
$INCLUDE C:\\Path_to_lib_script\myScript.vbs
```
The imported script relative path will be based on the open model parent folder. To use paths relevant to the running script paths, the `%RunningScriptPath%` token can be used.
For example, some useful functions have been defined in the `shared\Helpers.vbs` script, which is imported in the provided examples through the following command:
```
$INCLUDE %RunningScriptPath%\shared\Helpers.vbs
```

## Script Recording

Users can easily create VBScripts by recording their actions within LUSAS. The procedure is as follows:

1. To start by recording a script select File > Script > Start Recording...
2. Carry out a series of operations.
3. Stop recording by selecting File > Script > Stop Recording
4. You can then edit the .lvb file before use.

## Associate *.lvb extension with VBScript in your IDE

Your Integrated Development Environment (IDE) or Text/Code Editor will not recognise `*.lvb` files as `VBScript` language files (`*.vbs`). If your IDE does not offer custom file extension association, `*.lvb` file can be renamed to `*.vbs` extension. LUSAS recognises both extensions when run as scripts within LUSAS.

### Visual Studio Code

To associate the lvb extension with `VBScript` and add basic language features for Visual Basic Scripts, follow these steps:
1. Install the VSC plug in `VBS` (published by *Sherpen*)
2. Open an `*.lvb` file with Visual Studio Code
3. Click on the "Plain Text" label at the lower right window corner
4. Select "Configure File Association for '.lvb'..."
5. Select "VBScript" from the list

### Notepad++

To associate the lvb extension with `VBScript`, follow these steps:
1. Navigate to Settings > Style Configurator...
2. Select `VB / VBS` from the Language list
3. Add `lvb` in the `User Ext.:` input and click `Save & Close`
4. Restart Notepad++

## 🔗 Relevant Links

- [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V21_1/LPI%20Customisation%20and%20Automation%20Guide.pdf) (LPI & VBS)
