# Installation Guide for Python & Jupiter Notebooks

## Setting up Python on Windows

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
   
   - Run `pip install pywin32` to install pywin32
   
   - Optionally, additional Python libraries used accross the repository examples can be installed running: `pip install pandas openpyxl matplotlib`

3. **Run Python script**:
   
   - In Command Prompt, run: `python example.py`

## Setting up Jupyter Notebook on Windows

Ensure that Python is already installed on your system, then follow these steps:

1. **Install Jupyter Notebook**:
   - Press `Win + R`, type `cmd` and press Enter (this opens the command prompt)
   - Run: `pip install notebook`
   - If you get a "pip not recognized" error, try: `python -m pip install notebook`
2. **Launch Jupyter Notebook**:
   - In Command Prompt, run: `jupyter notebook`
   - Your browser should open automatically with Jupyter running
   - The notebook will run at [http://localhost:8888](http://localhost:8888)

**Alternative Method (Using Anaconda)**:
If you prefer a more comprehensive scientific Python environment:

1. Download and install Anaconda from [anaconda.com](https://anaconda.com)
2. After installation, launch "Anaconda Navigator"
3. Click on the Jupyter Notebook tile to launch it

## Install LUSAS Plugin Visual Studio Template

blablabla