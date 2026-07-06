# LPython Examples

LUSAS Python Script (*LPython*) code (files with *.lpy extensions) can be executed within LUSAS (v23+) through the Main Menu shortcut "Run Script" (red folder icon). These scripts are Python scripts that are executed inside LUSAS as opposed to normal Python script that are executed externally (see [python section](../python/README.md)).

## 📚 Examples Included

| Category   | Description                           | File                     |
| ---------- | ------------------------------------- | ------------------------ |
| General    | Create new model                      | 02_Create_New_Model.py |
| Geometry   | Creates points                        | 03_Point_Creation.py   |
| Tools      | FCM Replace Multiple Varying with Tapered Sections | FCM Replace Multiple Varying with Tapered Sections.lpy |

## 📄 Code

Scripts should always start with the `$ENGINE=LPython` command. Since LPython is executed internally, the code has direct access to all IFModeller methods some of which are listed bellow:

- `database()` or `db()`

- `selection()`

- `view()`

- `visible()`

- `newObjectSet()`

- `geometryData()` and `newGeometryData()`

- `getTextWindow().writeLine("Hello world!")` or `textWin().writeLine("Hello world!")`

The script relative path will be based on the open model parent folder.

Mind that Python `print()` command does not write on LUSAS's text window, instead use `getTextWindow().writeLine("My text")`.

## Using Python Packages in LPython scripts

LUSAS v23+ ships with an integrated Python installation located at `C:\ProgramData\Lusas230\x64\Python\` (the 32bit version is under `x86` folder). If you want to use additional libraries in LPython scripts, you need to install them into that Python environment.

First, install `pip` from a terminal (this is only required once):

```bat
cd C:\ProgramData\Lusas230\x64\Python\
python.exe get-pip.py
```

Then install the wishes library, i.e. `pandas`:

```bat
C:\ProgramData\Lusas230\x64\Python\python.exe -m pip install pandas
```

Mind that these Python environments changes for each LUSAS installation, between 32/64 bit versions and are removed upon uninstall. That's why it is recommended that Python scripts are executed externally (see [Python section](../python/)) where the system's Python version is used.

## ▶️ Script Shortcuts in LUSAS (toolbar button, menu item)

You can add your scripts in LUSAS toolbar or menu through the following steps.

**Toolbar button**:
1. Within LUSAS, navigate to the menu View > Toolbars.
2. Under the `User` tab, you can define up to 9 commands as single line *VBScript* (e.g. `msgbox "Hello world!"`) or call a script file (e.g. `fileopen "C:\LUSAS Scripts\MyScript.lpy"`)
3. Go back to the `Commands` tab and select `User` from the Categories list, and Drag & Drop one of the user buttons in one of the existing toolbars, then close the window.
4. You can edit the button icon by right clicking the toolbar button and selecting Button Appearance. Alternatively, you can modify the default user button icons by editing the following image `C:\\Path_to_my_lusas_installation\Programs\Config\userToolbar.bmp`.

The above commands assume that the Modeller's command bar language is set to VBScript (default).

**Menu item**:
1. Navigate to `%userprofile%\Documents\Lusas230\UserScripts` and edit the `UserMenu.vbs` or create a new if it does not exist.
2. This script will modify the LUSAS menu and the code should look like the following example:
```VBScript
$ENGINE=VBSCRIPT

' Create a user menu to host all menu entries
set myMenu = menu.appendMenu("User Menu")
' Create a new menu item
call myMenu.appendItem("Find attribute type", "fileopen ""C:\LUSAS Scripts\04f_Get_attribute_type_by_name.lpy"" " )
call myMenu.appendItem("Show attribute properties", "fileopen ""C:\LUSAS Scripts\04g_Extract_attribute_values.lpy"" " )
```

## 📝 Associate *.lpy extension with Python in your IDE

Your Integrated Development Environment (IDE) or Text/Code Editor will not recognise `*.lpy` files as *Python* language files (`*.py`). If your IDE does not offer custom file extension association, `*.lpy` file can be renamed to `*.py` extension.

### Visual Studio Code

To associate the lpy extension with *Python* and add basic language features for Visual Basic Scripts, follow these steps:
1. Open an `*.lpy` file with Visual Studio Code
2. Click on the `Plain Text` label at the lower right window corner
3. Select `Configure File Association for '.lpy'...`
4. Select `Python` from the list

### Notepad++

To associate the lpy extension with *Python*, follow these steps:
1. Navigate to Settings > Style Configurator...
2. Select `Python` from the Language list
3. Add `lpy` in the `User Ext.:` input
4. Click `Save & Close`
5. Restart Notepad++ (already open scripts may need to be closed)
