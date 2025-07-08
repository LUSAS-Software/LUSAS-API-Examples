# Python Examples

This folder contains Python scripts that interact with LUSAS creating model features or accessing analysis results.

It is recommended that beginners start from the `Jupyter Notebook` folder, which contains a plethora of examples in a friendly Notebook framework of Python blocks.

## 📚 Examples Included

| Category   | Description                           | File                   |
| ---------- | ------------------------------------- | ---------------------- |
| General    | Connects on LUSAS instance            | 01_Connect_to_LUSAS.py |
| General    | Create new model                      | 02_Create_New_Model.py |
| Geometry   | Creates points                        | 03_Point_Creation.py   |
| Geometry   | Creates lines                         | 04_Line_Creation.py    |
| Geometry   | Creates surfaces                      | 05_Surface_Creation.py |
| Geometry   | Creates volumes                       | 06_Volume_Creation.py  |
| Geometry   | Use ObjectSets (Database, Groups, Selection etc) and filter geometries | 07_Get_Geometries_Groups_Selection_ObjectSets.py |
| Attributes | Create/assign meshes                 | 10_Create_and_assign_mesh.py     |
| Attributes | Create/assign sections               | 11_Create_and_assign_section.py  |
| Attributes | Create/assign materials              | 12_Create_and_assign_material.py |
| Attributes | Create/assign supports               | 13_Create_and_assign_supports.py |
| Attributes | Create/assign loads                  | 14_Create_and_assign_loads.py    |
| Attributes | Create a simply supported beam       | 15_Simply_Supported_Beam.py      |
| Attributes | Extract geometric properties of lines (beams) and surfaces. | 18_Extract_Geometric_Properties.py |
| Analyses   | Create/solve analyses and loadcases  | 20_Create_and_Run_Analyses_and_Loadcases.py |
| Analyses   | Create Combinations and Envelopes    | 21_Create_Combinations_and_Envelopes.py |
| Analyses   | Create Coupled Structural-Thermal Analysis        | 22_Coupled_Structural_Thermal_Analysis.py |
| Results    | Get results from Elements/Nodes                   | 30_Getting_Results.py     |
| Results    | Get results with Print Results Wizard             | 31_Getting_Results_PRW.py |
| Results    | Create User Defined Results and Design Attributes | 32_User_Defined_Results_and_Design_Attributes.py |


## ⚙️ Setting up Python on Windows

You can first **check if Python is already installed** on your system through one of the following methods:

1. **Using Command Prompt**:
   - Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
   - Type `python --version` or `python -V` and press Enter
   - If Python is installed, you'll see the version number (like "Python 3.13.3")
   - You can also try `py --version` as an alternative
2. **From the Start Menu**:
   - Search for "Python" in your Start menu
   - If Python is installed, you should see it listed

To **install Python** on your system, follow these steps:

1. **Install Python**:
   
   - Download a Python installer from [python.org](https://python.org), preferably v3.13.*
   
   - During installation, make sure to **check "Add Python to PATH"**
   
   - Complete the installation process

2. Install required Python **libraries**:
   
   - Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
   
   - To install **pywin32**, run:
     
     ```bash
     pip install pywin32==308
     ```
   
   - Optionally, additional Python libraries used across the repository examples can be installed running:
     
     ```bash
     pip install pandas openpyxl matplotlib
     ```

If you are using *Visual Studio Code* as your (IDE), it is recommended that you also install the `Python` and `Pylance` plugin (released by *Microsoft*).

## 🚀 How to Run

Python can be executed in the traditional way, outside LUSAS, or similarly to *VBScripts*, through the Main Menu shortcut "Run Script".

The examples in this directory assume that Python will connect on LUSAS externally. The connection will be established through the Component Object Model (COM) system, similarly to connecting on other software like MS Excel. A Python script can be run externally with the following CMD command: 

```bash
cd LUSAS-API-Examples/python/
python create_beam_model.py
```

## ▶️ Script Shortcuts in LUSAS (toolbar button, menu item)

You can add your scripts in LUSAS toolbar or menu through the following steps.

**Toolbar button**:
1. Within LUSAS, navigate to the menu View > Toolbars.
2. Under the `User` tab, you can define up to 9 commands where you can call you python script file with the following command:
```VBScript
' With command prompt shown
CreateObject("WScript.Shell").Run "py C:\\path_to_my_script\myScript.py"
' Or with command prompt hidden
CreateObject("WScript.Shell").Run "py C:\\path_to_my_script\myScript.py", 0, true
```
3. Go back to the `Commands` tab and select `User` from the Categories list, and Drag & Drop one of the user buttons in one of the existing toolbars, then close the window.
4. You can edit the button icon by right clicking the toolbar button and selecting Button Appearance. Alternatively, you can modify the default user button icons by editing the following image `C:\\Path_to_my_lusas_installation\Programs\Config\userToolbar.bmp`.

**Menu item**:
1. Navigate to `%userprofile%\Documents\Lusas220\UserScripts` and edit the `UserMenu.vbs` or create a new if it does not exist.
2. This script should modify the LUSAS menu and the code should look like the following example:
```VBScript
$ENGINE=VBSCRIPT

' Create a user menu to host all menu entries
set myMenu = menu.appendMenu("User Menu")
' Create a new menu item
call myMenu.appendItem("My script (cmp shown)", "CreateObject(""WScript.Shell"").Run ""py C:\\path_to_my_script\myScript.py"" " )
call myMenu.appendItem("My script (cmp hidden)", "CreateObject(""WScript.Shell"").Run ""py C:\\path_to_my_script\myScript.py"", 0, true" )
```

## 🔍🐛 Troubleshooting

1. **Command prompt error `python: command not found` or `The term 'python' is not recognized`**

   This error is thrown when the python installation path is not in the Windows `PATH`. To solve this, follow these steps:
   - In the Windows search bar, type python 3 and right-click on the first found item (e.i. `Python 3.13.3 (32bit)`) selecting `Open file location`. If no items are found, then python is not install on the machine.
   - In the open folder, right-click on the highlighted file (e.g. `Python 3.10 (32-bit)`) and select `Open file location` again. 
   - In the open folder, verify that you see the `python.exe`. Copy the folder path and close the folder.
   - On your desktop, right click on `This PC` and select `Properties`.
   - In the open window, find and click the `Advanced system settings` link to open the System Properties.
   - In the open window, click on `Environment Variables...`, and under the User Variables, select the `Path` variable and click edit.
   - In the open window, click `new` and paste the copied python path.
   - Click OK on all windows to close them.
   - Now you can run python commands in the command prompt.

2. **Python error `AttributeError: module 'win32com.gen_py.XXXXXXXXXXXXXXXX' has not attribute 'CLSIDToClassMap'`** (How to delete pyWin32 cache)

   First, ensure that you are using the `LPI.py` or `LPI_22_0.py` library and that the object at the error line has the called method.
   Python is case sensitive which may sometimes cause issues with pywin32. These issues are usually fixed by deleting the pywin32 cache. To do so, follow these steps:
   - Navigate to `%TEMP%/gen_py` and open the python version folder (e.g. 3.13)
   - Delete the folder that matches the error message `XXXXXXXXXXXXXXXX`
   - Run the script again.

3. **Invisible LUSAS Modeller instances**

   To speed-up the script execution, the UI can be disabled using the `lusas.setVisible(False)` command. This will completely hide LUSAS modeller which can cause confusion if the `lusas.setVisible(True)` command is not executed at the end of the script (e.g. due to a code error). The modeller instance would still be accessible through the LPI and its process will be listed under the `Background processes` in Window's `Task Manager`.
   
   It is noted that in LUSAS v22+, it may be preferable to use `lusas.enableUI(False)` instead to avoid hiding the modeller window. The UI will then remain unresponsive until `lusas.enableUI(True)` is called.

4. **ModuleNotFoundError**

   The `ModuleNotFoundError: No module named 'shared'` error means Python can’t find the `LPI.py` file and the `shared` folder. To fix it, copy the `shared` folder into the same folder where your Python script is located.

## 🔍 Tips for Advanced Users

1. **Early and Late binding**

   There are 3 ways to connect on COM applications using pyWin32 which will affect the type of the returned objects:
   - `win32com.client.Dispatch("Application")` returns a COM object or a win32com.gen_py object if the object is already cached.
   - `win32com.client.gencache.EnsureDispatch.Dispatch("Application")` (early binding) returns a win32com.gen_py object.
   - `win32com.client.dynamic.Dispatch("Application")` (late binding) returns a COM object.

   The `get_lusas_modeller()` command used in the provided examples connects on LUSAS using the `win32com.client.dynamic.Dispatch()`.
   This is preferred as object casting is not required and requested methods are handled directly by the connected application as opposed to the generated Python cache.

2. **pyWin32 Casting** (when early binding is used)

   Some LPI commands will return the general object types.
   When late binding is used, casting is not required to access methods available in sub classes (e.g. for IFLoadcase but not for IFLoadset).
   When early binding is used, casting is required to avoid errors raised by the generated classes in the win32com cache. As an example, getting a loadcase object can be done through the `getLoadsetByName()` command which will return an `IFLoadset` object. If you are sure that this object is a loadcase, you can cast it as an `IFLoadcase` object using the command `win32com.client.CastTo(myLoadset, "IFLoadcase")`. This is also commonly done when accessing attributes through the `getAttribute()` LPI command, for example when acquiring a Print Results Wizard it would need to be cast from an IFAttribute to an `IFPrintResultsWizard`.

3. **Architecture of COM launched LUSAS Modeller instance (32/64bit)**

   To change the preferred LUSAS Modeller architecture when LUSAS is launched through COM, run one of the following commands in CMD with admin permissions:
   - To follow the architecture of the parent process:

      ```REG ADD HKEY_CLASSES_ROOT\AppID\{AC0CF860-2200-11CF-91D8-0020AFC19F64} /t REG_DWORD /v PreferredServerBitness /d 00000001 /f```

   - To always call the 32bit:

      ```REG ADD HKEY_CLASSES_ROOT\AppID\{AC0CF860-2200-11CF-91D8-0020AFC19F64} /t REG_DWORD /v PreferredServerBitness /d 00000002 /f```

   - To always call the 64bit:

      ```REG ADD HKEY_CLASSES_ROOT\AppID\{AC0CF860-2200-11CF-91D8-0020AFC19F64} /t REG_DWORD /v PreferredServerBitness /d 00000003 /f```

   Alternatively, manually launch LUSAS so that COM connects on that specific running instance.

## 🔗 Links

- [Python Official Site](https://www.python.org/)
- [pywin32 Github](https://github.com/mhammond/pywin32)
