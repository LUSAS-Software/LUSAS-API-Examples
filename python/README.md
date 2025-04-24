# Python Examples

This folder contains Python scripts that interact with LUSAS creating model features or accessing analysis results.

It is recommended that beginners start from the `Jupyter Notebook` folder, with contains a plethora of examples in a friendly Notebook framework of Python blocks.

## 📚 Examples Included

| Category | Description                           | Language   | File                    |
| -------- | ------------------------------------- | ---------- | ----------------------- |
| General  | Connects on LUSAS instance            | Python     | 01a_Connect_on_LUSAS.py |
| General  | Create new model                      | Python     | 01b_Create_New_Model.py |
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


## ⚙️ Setting up Python on Windows

You can first **check if Python is already installed** on your system through one of the following methods:

1. **Using Command Prompt**:
   - Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
   - Type `python --version` or `python -V` and press Enter
   - If Python is installed, you'll see the version number (like "Python 3.10.5")
   - You can also try `py --version` as an alternative
2. **From the Start Menu**:
   - Search for "Python" in your Start menu
   - If Python is installed, you should see it listed

To **install Python** on your system, follow these steps:

1. **Install Python**:
   
   - Download the latest Python installer from [python.org](https://python.org)
   
   - During installation, make sure to **check "Add Python to PATH"**
   
   - Complete the installation process

2. Install required Python **libraries**:
   
   - Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
   
   - To install **pywin32**, run:
     
     ```bash
     pip install pywin32
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

## 🔗 Links

- [Python Official Site](https://www.python.org/)
- [pywin32 Github](https://github.com/mhammond/pywin32)
