# VBScript Examples

Visual Basic Script (VBScript) code (files with *.vb or *.lvb extensions) can be excecuted within LUSAS through the Main Menu shortcut "Run Script" (red folder icon).

## 📚 Examples Included

| Category | Description                       | Language   | File                 |
| -------- | --------------------------------- | ---------- | -------------------- |
| Geometry | Create a simple beam and 2D frame | Python/VBS | create_beam_model.py |

## Code

Scripts should always start with the `$ENGINE=VBScript` command. Since VBScript is excecuted internally, code has direct access to the following methods:

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

## 🔗 Relevant Links

- [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V21_1/LPI%20Customisation%20and%20Automation%20Guide.pdf) (LPI & VBS)
