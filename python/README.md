# Python Examples

This folder contains Python scripts that interact with LUSAS creating model features or accessing analysis results.

It is recommended that beginers start from the `Jupyter Notbook` folder, with contains a plethora of examples in a friendly Notbook framework or Python blocks.

## 📚 Examples Included

| Category         | Description                            | Language       | File                        |
| ---------------- | -------------------------------------- | -------------- | --------------------------- |
| Geometry         | Create a simple beam and 2D frame      | Python/VBS     | create_beam_model.py        |

## ⚙️ Setting up Python on Windows

You can first **check if Python is already installed** on your system through one of the follwoing methods:

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
   
   - Optionally, additional Python libraries used accross the repository examples can be installed running:
     
     ```bash
     pip install pandas openpyxl matplotlib
     ```

## 🚀 How to Run

Python can be excecuted in the traditional way, outside LUSAS, or similarly to *VBScripts*, through the Main Menu shortcut "Run Script".

The examples in this directory assume that Python will connect on LUSAS externally. The connection will be established through the Component Object Model (COM) system, silarly to connecting on other software like MS Excel. A Python script can be run externally with the following CMD command: 

```bash
cd LUSAS-API-Examples/python/
python create_beam_model.py
```



## 🔗 Links

- [Python Official Site](https://www.python.org/)
- [pywin32 Github](https://github.com/mhammond/pywin32)
- [Grasshopper LUSAS plug in]([LUSAS_Grasshopper | Food4Rhino](https://www.food4rhino.com/en/app/lusasgrasshopper))
