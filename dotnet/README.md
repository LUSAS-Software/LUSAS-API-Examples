# .NET Examples (C# and VB.NET)

This folder contains information about connecting to LUSAS and LPI through .NET (e.i. VB.NET and C#). 

### 🚀 Why Use .NET Over a Scripting Language?

While VBScript is useful for simple automation and quick scripting, compiled languages like **VB.NET** and **C#** provide additional power and flexibility, especially for more complex applications such as custom dialogs or plugins.

### 🔑 Key Advantages of VB.NET over VBScript

- Rich **User Interface creation** (dialogs, forms, wizards)
- Built-in **debugging** with breakpoints and error tracing
- **Extensible and maintainable** through Object-Oriented Programming (OOP)
- Distribute as a single `.dll` or `.exe` instead of multiple script files
- Easier **unit testing** and reuse across projects

VB.NET is especially suitable if you're already familiar with VBScript syntax and want to build more robust, user-friendly tools without needing deep knowledge of COM or C++.

## 📚 Repository Examples

| Name         | Description                                                                                          | Language     | Repository                                  |
| ------------ | ---------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------- |
| LusasToolkit | A set of custom functionalities (e.g. copy assignments, generate combinations from spreadsheets etc) | C# / Plugin | https://github.com/CadairIdris/LusasToolkit |
| LUSAS-Lookup | Inspection of the LUSAS' database and the available methods of each object                           | C# / Plugin | https://github.com/GreatApo/LUSAS-Lookup    |

## ⚙️ Setting up

To work with VB.NET or C#, you need an IDE and a compiler. We recommend using [Visual Studio 2019](https://www.visualstudio.com/downloads) that combines both.

Projects can be compiled as:
- executables (`.exe`) that can externally connect on LUSAS through COM and do not require any additional setup,
- libraries (`.dll`) that can be loaded in LUSAS as custom modules (plugins).

To easily create new plugin projects in Visual Studio, the LUSAS project template can used:
1. Copy the `LusasModule22_0.zip` file from the LUSAS installation directory `<LUSAS Installation Folder>\LUSAS220\Programs (x86)` to the Visual Studio project template folder `%USERPROFILE%\Documents\Visual Studio 2019\Templates\ProjectTemplates\Visual Basic`
2. Open Visual Studio and select `File` > `Create a new Project`
3. Scroll to the bottom and select the `LUSAS Module 22.0` template from the available list, and click `Next`
4. Pick a project name and click create.
5. After writing and compiling your project as a library (`.dll`), you can configure LUSAS to automatically import it through the following steps:
   - Move the `.dll` in `%USERPROFILE%\Documents\Lusas220\Modules`
   - Create an `.lml` text file next to your library, with the same name and the following contents:
```xml
<?xml version="1.0" encoding="utf-8"?>
<modules xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" domain="My_Project_Name.AutoConfig" version="1.0.0" xmlns="urn:lusas:modules:1.0">
  <module name="My_Project_Name">
    <assembly>
      <path>%ModulesUserDir%</path>
      <file>My_Project_Name.dll</file>
      <class>Lusas.My_Project_Name.MainModule</class>
    </assembly>
    <identity>
      <friendlyname>My Project Name</friendlyname>
      <description>My_Project_Name - LUSAS Extension Module</description>
    </identity>
    <keys />
    <verified />
    <options>
      <decrypt>true</decrypt>
      <verbose>true</verbose>
      <debug>true</debug>
      <kid>1</kid>
    </options>
  </module>
</modules>
```

More information can be found in the [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V22_0/LPI%20Customisation%20and%20Automation%20Guide.pdf).

## 🔗 Links

- [LUSAS LPI Customisation and Automation Guide](https://www.lusas.com/user_area/documentation/V22_0/LPI%20Customisation%20and%20Automation%20Guide.pdf) (LPI, VBS, VB.NET)
