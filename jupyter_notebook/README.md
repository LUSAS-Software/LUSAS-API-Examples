# Jupyter Notebook Examples

This directory includes plethora of examples going through most of the LPI. Jupyter Notebook examples is the recommended way to interact will LUSAS for beginers.

## ⚙️Setting up Python on Windows

You can first check if Python is already installed on your system through one of the follwoing methods:

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
   
   - Run `pip install pywin32 ipykernel` to install pywin32 and ipykernel (default kernel used by Jupyter Notebooks)
   
   - Optionally, additional Python libraries used accross the repository examples can be installed running: `pip install pandas openpyxl matplotlib`

## ⚙️Setting up Jupyter Notebook on Windows

Ensure that Python is already installed on your system, then follow these steps:

**Install Jupyter Notebook**:

- Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
- Run: `pip install notebook`
- If you get a "pip not recognized" error, try: `python -m pip install notebook` 

## 🚀 How to Run

#### Visual Studio Code

The easiest way to run Jupyter Notebook scripts is by opening the with *Visual Studio Code*. Each code block can be excecuted by the run shortcut ▶️ next to them. It is adviced that all code blocks are run from top to bottom.

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

1. Install the library: `pip install nbconvert`
2. Convert your script: `jupyter nbconvert --to script myNotebook.ipynb` (use your notebook filename instead of `myNotebook.ipynb`)

To convert all notebooks within a folder, the following command can be used: `jupyter nbconvert --to script *.ipynb`