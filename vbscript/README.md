# VBScript Examples

Visual Basic Script (*VBScript*) code (files with *.vb or *.lvb extensions) can be executed within LUSAS through the Main Menu shortcut "Run Script" (red folder icon). One line *VBScript* commands can also be executed through LUSAS's command bar (by default is set to *VBScript*). To enable the command bar, navigate to View > LPI Command Bar.

## 📚 Examples Included

| Category   | Description                           | File                     |
| ---------- | ------------------------------------- | ------------------------ |
| General    | Create new model                      | 01_Create_New_Model.lvb |
| Geometry   | Creates points                        | 03_Point_Creation.lvb   |
| Geometry   | Creates lines                         | 04_Line_Creation.lvb    |
| Geometry   | Creates surfaces                      | 05_Surface_Creation.lvb |
| Geometry   | Creates volumes                       | 06_Volume_Creation.lvb  |
| Geometry   | Use ObjectSets (Database, Groups, Selection etc) and filter geometries | 07_Get_Geometries_Groups_Selection_ObjectSets.lvb |
| Attributes | Create/assign meshes                  | 10_Create_and_assign_mesh.lvb     |
| Attributes | Create/assign sections                | 11_Create_and_assign_section.lvb  |
| Attributes | Create/assign materials               | 12_Create_and_assign_material.lvb |
| Attributes | Create/assign supports                | 13_Create_and_assign_supports.lvb |
| Attributes | Create/assign loads                   | 14_Create_and_assign_loads.lvb    |
| Attributes | Create a simply supported beam        | 15_Simply_Supported_Beam.lvb      |
| Attributes | Extracts all attributes' properties in a data grid or CSV for the user given attribute names (UI input) | 16_Extract_attribute_values.lvb |
| Attributes | Prints the attribute type(s) for the user given attribute names (UI input) | 17_Get_attribute_type_by_name.lvb |
| Attributes | Extract geometric properties of lines (beams) and surfaces | 18_Extract_Geometric_Properties.lvb |
| Analyses   | Create/solve analyses and loadcases   | 20_Create_and_Run_Analyses_and_Loadcases.lvb |
| Analyses   | Create Combinations and Envelopes     | 21_Create_Combinations_and_Envelopes.lvb |
| Analyses   | Create Coupled Structural-Thermal Analysis | 22_Coupled_Structural_Thermal_Analysis.lvb |
| Results    | Get results from Elements/Nodes            | 30_Getting_Results.lvb     |
| Results    | Get results with Print Results Wizard      | 31_Getting_Results_PRW.lvb |

More examples can be found in your LUSAS installation folder at `<lusas_installation_path>\LUSAS211\Programs\scripts\LPIExamples`.

## 📄 Code

Scripts should always start with the `$ENGINE=VBScript` command. Since VBScript is executed internally, the code has direct access to all IFModeller methods some of which are listed bellow:

- `database()` or `db()`

- `selection()`

- `view()`

- `visible()`

- `newObjectSet()`

- `geometryData()` and `newGeometryData()`

- `getTextWindow().writeLine("Hello world!")` or `textWin.writeLine("Hello world!")`

Since VBScript does not natively support imports, the following command can be used at the top of `*.lvb` files to import other scripts:
```
$INCLUDE C:\\Path_to_lib_script\myScript.vbs
```
The imported script relative path will be based on the open model parent folder. To use paths relevant to the running script paths, the `%RunningScriptPath%` token can be used.
For example, some useful functions have been defined in the `shared\Helpers.vbs` script, which is imported in the provided examples through the following command:
```
$INCLUDE %RunningScriptPath%\shared\Helpers.vbs
```

## 🔴 Script Recording

Users can easily create VBScripts by recording their actions within LUSAS. The procedure is as follows:

1. To start by recording a script select File > Script > Start Recording...
2. Carry out a series of operations.
3. Stop recording by selecting File > Script > Stop Recording
4. You can then edit the .lvb file before use.

## ▶️ Script Shortcuts in LUSAS (toolbar button, menu item)

You can add your scripts in LUSAS toolbar or menu through the following steps.

**Toolbar button**:
1. Within LUSAS, navigate to the menu View > Toolbars.
2. Under the `User` tab, you can define up to 9 commands as single line *VBScript* (e.g. `msgbox "Hello world!"`) or call a script file (e.g. `fileopen "C:\LUSAS Scripts\MyScript.vbs"`)
3. Go back to the `Commands` tab and select `User` from the Categories list, and Drag & Drop one of the user buttons in one of the existing toolbars, then close the window.
4. You can edit the button icon by right clicking the toolbar button and selecting Button Appearance. Alternatively, you can modify the default user button icons by editing the following image `<lusas_installation_path>\Programs\Config\userToolbar.bmp`.

**Menu item**:
1. Navigate to `%userprofile%\Documents\Lusas211\UserScripts` and edit the `UserMenu.vbs` or create a new if it does not exist.
2. This script should modify the LUSAS menu and the code should look like the following example:
```VBScript
$ENGINE=VBSCRIPT

' Create a user menu to host all menu entries
set myMenu = menu.appendMenu("User Menu")
' Create a new menu item
call myMenu.appendItem("Find attribute type", "fileopen ""C:\LUSAS Scripts\04f_Get_attribute_type_by_name.lvb"" " )
call myMenu.appendItem("Show attribute properties", "fileopen ""C:\LUSAS Scripts\04g_Extract_attribute_values.lvb"" " )
```

## 📝 Associate *.lvb extension with VBScript in your IDE

Your Integrated Development Environment (IDE) or Text/Code Editor will not recognise `*.lvb` files as *VBScript* language files (`*.vbs`). If your IDE does not offer custom file extension association, `*.lvb` file can be renamed to `*.vbs` extension. LUSAS recognises both extensions when run as scripts within LUSAS.

### Visual Studio Code

To associate the lvb extension with *VBScript* and add basic language features for Visual Basic Scripts, follow these steps:
1. Install the VSC plug in `VBS` (published by *Sherpen*)
2. Open an `*.lvb` file with Visual Studio Code
3. Click on the `Plain Text` label at the lower right window corner
4. Select `Configure File Association for '.lvb'...`
5. Select `VBScript` from the list

### Notepad++

To associate the lvb extension with *VBScript*, follow these steps:
1. Navigate to Settings > Style Configurator...
2. Select `VB / VBS` from the Language list
3. Add `lvb` in the `User Ext.:` input
4. Click `Save & Close`
5. Restart Notepad++

## 🔗 Relevant Links

- [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V21_1/LPI%20Customisation%20and%20Automation%20Guide.pdf) (LPI & VBS)
