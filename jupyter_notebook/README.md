# Jupyter Notebook Examples

This directory includes plethora of examples going through most of the LPI. Jupyter Notebook examples is the recommended way to interact will LUSAS for beginners.

## 📚 Examples Included

| Category   | Description                                                     | File                          |
| ---------- | --------------------------------------------------------------- | ----------------------------- |
| General    | Connects on LUSAS instance                                      | 01 Getting Connected.ipynb    |
| General    | Handle string parsing and returned values                       | 02 Expression Parsing and Return values.ipynb |
| Geometry   | Creates points, lines, surfaces and volumes                     | 03 Geometry creation.ipynb    |
| Geometry   | Use ObjectSets (Database, Groups, Selection etc) and filter geometries | 04 Get Geometries, Groups, Selection and ObjectSets.ipynb |
| Geometry   | Creates a simple multistorey 3D Frame geometry out of lines     | 05 Simple 3D Frame.ipynb      |
| Attributes | Creates and solves a steel beam cantilver model by creating basic mesh, geometric, material, support and loading attributes. | 10 Simple Cantilever beam.ipynb |
| Attributes / Results | Creates and solves a steel beam simply supported model and procceses the results. | 11 Simply Supported Line Beam.ipynb |
| Attributes | Extract all the values of geometric or material attributes in formats that are easier for reviewing and checking models (e.g. spreadsheets) | 16 Extract Attribute Values.ipynb |
| Attributes | Creates a 2D bridge with rigid constraints (links) between deck beams and pier legs. | 17 Rigid Constraints.ipynb |
| Attributes | Use of design attributes to hold user data                      | 18 Design Attributes.ipynb    |
| Results    | Get results from Elements/Nodes                                 | 30 Getting Results.ipynb      |
| Results    | Create Print Result Wizards and export to spreadsheets and txts | 31 Getting Results PRW.ipynb  |
| Results    | Create User Defined Results                                     | 32 User Defined Results.ipynb |

Additional examples are included in the `Tools` and `Wizards` folders.

## ⚙️Setting up Python on Windows

You can first check if Python is already installed on your system through one of the following methods:

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
   
   - Run the following command to install pywin32 and ipykernel (default kernel used by Jupyter Notebooks)
      ```bash
      pip install pywin32==308 ipykernel
      ```
   
   - Optionally, additional Python libraries used across the repository examples can be installed running:
      ```bash
      pip install pandas openpyxl matplotlib numpy
      ```

## ⚙️Setting up Jupyter Notebook on Windows

Ensure that Python is already installed on your system, then follow these steps:

**Install Jupyter Notebook**:

- Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)

- Run:
   ```bash
   pip install notebook
   ```

- If you get a `pip not recognized` error, try:
   ```bash
   python -m pip install notebook
   ```

## 🚀 How to Run

#### Visual Studio Code

The easiest way to run Jupyter Notebook scripts is by opening the with *Visual Studio Code*. Each code block can be executed by the run shortcut ▶️ next to them. It is advised that all code blocks are run from top to bottom.

You will need to install the following VSCode plugins:

- `Python` plugin (released by *Microsoft*)

- `jupyter` plugin (released by *Microsoft*)

- Optionally, `Pylance` plugin (released by *Microsoft*)

#### Manually

Launch Jupyter Notebook:

- In Command Prompt, run: `jupyter notebook`
- Your browser should open automatically with Jupyter running
- The notebook will run at [http://localhost:8888](http://localhost:8888)

##### Using Anaconda:

If you prefer a more comprehensive scientific Python environment:

1. Download and install Anaconda from [anaconda.com](https://anaconda.com)
2. After installation, launch "Anaconda Navigator"
3. Click on the Jupyter Notebook tile to launch it

## Convert Jupyter Notebooks to Python scripts

If you want to convert your Jupyter Notebooks to Python scripts, you can do so through the `nbconvert` library:

1. Install the library:
   ```bash
   pip install nbconvert
   ```

2. Convert your script: (use your notebook filename instead of `myNotebook.ipynb`)
   ```bash
   jupyter nbconvert --to script myNotebook.ipynb
   ```
   To convert all notebooks within a folder, the following command can be used:
   ```bash
   jupyter nbconvert --to script *.ipynb
   ```