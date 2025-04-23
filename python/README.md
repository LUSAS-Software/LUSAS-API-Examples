# Python Examples

This folder contains Python scripts that interact with LUSAS creating model features or accessing analysis results.

It is recommended that beginners start from the `Jupyter Notebook` folder, with contains a plethora of examples in a friendly Notebook framework of Python blocks.

## 📚 Examples Included

| Category | Description                       | Language   | File                 |
| -------- | --------------------------------- | ---------- | -------------------- |
| Geometry | Create a simple beam and 2D frame | Python     | create_beam_model.py |

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
- [Grasshopper LUSAS plug in](https://www.food4rhino.com/en/app/lusasgrasshopper)
