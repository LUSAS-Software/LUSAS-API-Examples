# VBScript Examples

Visual Basic Script (VBScript) code (files with *.vb or *.lvb extensions) can be executed within LUSAS through the Main Menu shortcut "Run Script" (red folder icon).

## 📚 Examples Included

| Category | Description                       | Language   | File                 |
| -------- | --------------------------------- | ---------- | -------------------- |
| Geometry | Create a simple beam and 2D frame | Python/VBS | create_beam_model.py |

## Code

Scripts should always start with the `$ENGINE=VBScript` command. Since VBScript is executed internally, code has direct access to the following methods:

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

## Associate *.lvb extension with VBScript in your IDE

Your Integrated Development Environment (IDE) or Text/Code Editor will not recognise `*.lvb` files as `VBScript` language files (`*.vbs`). If your IDE does not offer custom file extension association, `*.lvb` file can be renamed to `*.vbs` extension. LUSAS recognises both extensions when run as scripts within LUSAS.

### Visual Studio Code

To associate the lvb extension with `VBScript`, follow these steps:
1. Open an `*.lvb` file with Visual Studio Code
2. Click on the "Plain Text" label at the lower right window corner
3. Select "Configure File Association for '.lvb'..."
4. Select "VBScript" from the list

### Notepad++

To associate the lvb extension with `VBScript`, follow these steps:
1. Navigate to Settings > Style Configurator...
2. Select `VB / VBS` from the Language list
3. Add `lvb` in the `User Ext.:` input and click `Save & Close`
4. Restart Notepad++

## 🔗 Relevant Links

- [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V21_1/LPI%20Customisation%20and%20Automation%20Guide.pdf) (LPI & VBS)
