# VBScript Examples

Visual Basic Script (VBScript) code (files with *.vb or *.lvb extensions) can be executed within LUSAS through the Main Menu shortcut "Run Script" (red folder icon).

## 📚 Examples Included

| Category | Description                       | Language   | File                 |
| -------- | --------------------------------- | ---------- | -------------------- |
| General  | Create new model                      | Python     | 01a_Create_New_Model.py |
| Geometry | Creates points                        | Python     | 02a_Point_Creation.py   |
| Geometry | Creates lines                         | Python     | 02b_Line_Creation.py    |
| Geometry | Creates surfaces                      | Python     | 02c_Surface_Creation.py |
| Geometry | Creates volumes                       | Python     | 02d_Volume_Creation.py  |
| Geometry | Use ObjectSets (Database, Groups, Selection etc) and filter geometries | Python     | 03_Get_Geometries_Groups_Selection_ObjectSets.py |
| Attributes | Create/assign meshes                | Python     | 04a_Create_and_assign_mesh.py     |
| Attributes | Create/assign sections              | Python     | 04b_Create_and_assign_section.py  |
| Attributes | Create/assign materials             | Python     | 04c_Create_and_assign_material.py |
| Attributes | Create/assign supports              | Python     | 04d_Create_and_assign_supports.py |
| Attributes | Create/assign loads                 | Python     | 04d_Create_and_assign_loads.py    |
| Analyses   | Create/solve analyses and loadcases | Python     | 05a_Create_and_Run_Analyses_and_Loadcases.py |
| Analyses   | Create Combinations and Envelopes   | Python     | 05b_Create_Combinations_and_Envelopes.py |
| Analyses   | Create Coupled Structural-Thermal Analysis | Python     | 05c_Coupled_Structural_Thermal_Analysis.py |
| Results    | Get results from Elements/Nodes            | Python     | 06a_Getting_Results.py     |
| Results    | Get results with Print Results Wizard      | Python     | 06b_Getting_Results_PRW.py |

## Code

Scripts should always start with the `$ENGINE=VBScript` command. Since VBScript is executed internally, code has direct access to the following methods:

- `database()` or `db()`

- `selection()`

- `view()`

- `visible()`

- `newObjectSet()`

- `geometryData()` and `newGeometryData()`

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
1. Install the VSC plug in `VBS` (published by Sherpen)
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
