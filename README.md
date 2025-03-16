# KiCad Symbol Generator and Electronic Components Database

This project consists of three main components: a Python script for generating KiCad symbol files, a web-based Resistors Database application, and a web-based Capacitors Database application.

## Table of Contents
- [KiCad Symbol Generator and Electronic Components Database](#kicad-symbol-generator-and-electronic-components-database)
  - [Table of Contents](#table-of-contents)
  - [KiCad Symbol Generator](#kicad-symbol-generator)
    - [Features](#features)
    - [Requirements](#requirements)
    - [Usage](#usage)
    - [CSV File Format](#csv-file-format)
  - [Electronic Components Database](#electronic-components-database)
    - [Deployment](#deployment)
    - [Resistors Database](#resistors-database)
      - [About](#about)
      - [Features](#features-1)
    - [Capacitors Database](#capacitors-database)
      - [About](#about-1)
      - [Features](#features-2)
    - [Usage Steps (for both Resistors and Capacitors Databases)](#usage-steps-for-both-resistors-and-capacitors-databases)
    - [Technical Details](#technical-details)
  - [Adding as a Submodule](#adding-as-a-submodule)
  - [Removing the Submodule](#removing-the-submodule)

## KiCad Symbol Generator

This Python script generates KiCad symbol files (.kicad_sym) for electronic components based on data from CSV files. It's designed to streamline the process of creating custom symbols for use in KiCad electronic design automation (EDA) software.

### Features

- Generates KiCad symbol files from CSV data
- Customizable for different component properties
- Creates standardized symbols with configurable properties
- Handles multiple components in a single CSV file

### Requirements

- Python 3.x
- No external libraries required (uses only Python standard library)

### Usage

1. Prepare your CSV file with component data (see `resistor.csv` or `capacitor.csv` for example formats).
2. Run the script:

   ```
   python kicad_symbol_generator.py
   ```

3. The script will generate a `.kicad_sym` file in the same directory.

### CSV File Format

The input CSV file should have the following headers:

- Symbol Name
- Reference
- Value
- Footprint
- Datasheet
- Description
- Manufacturer
- MPN
- Tolerance
- Voltage Rating

Each row in the CSV represents a different resistor.

## Electronic Components Database

The Electronic Components Database consists of two web applications: the Resistors Database and the Capacitors Database. These applications provide interactive interfaces for viewing and managing databases of electronic components.

### Deployment

Both database applications are deployed and accessible at:

https://kicad-symbol-generator.onrender.com

You can visit this URL to interact with the live versions of the applications.

### Resistors Database

#### About

The Resistors Database is an interactive web application that provides a comprehensive view of resistor specifications. It allows users to easily browse, search, and filter through a database of resistors, providing quick access to important information and datasheets.

#### Features

- Interactive data table displaying resistor specifications
- Dynamic filtering and multi-column sorting capabilities
- Pagination for efficient browsing of large datasets
- Direct links to resistor datasheets
- Responsive design adapting to light and dark themes
- Easy-to-use interface for exploring resistor data

### Capacitors Database

#### About

The Capacitors Database is an interactive web application that provides a comprehensive view of capacitor specifications. It allows users to easily browse, search, and filter through a database of capacitors, providing quick access to important information and datasheets.

#### Features

- Interactive data table displaying capacitor specifications
- Dynamic filtering and multi-column sorting capabilities
- Pagination for efficient browsing of large datasets
- Direct links to capacitor datasheets
- Responsive design adapting to light and dark themes
- Easy-to-use interface for exploring capacitor data

### Usage Steps (for both Resistors and Capacitors Databases)

1. Navigate to the Electronic Components Database page at https://kicad-symbol-generator.onrender.com
2. Choose either the Resistors Database or Capacitors Database from the navigation menu
3. Use the table's built-in search functionality to find specific components
4. Click on column headers to sort the data
5. Use the filter action to narrow down the displayed results
6. Navigate through pages using the pagination controls at the bottom of the table
7. Access component datasheets by clicking on the provided links in the 'Datasheet' column
8. Switch between light and dark themes for comfortable viewing in different environments

### Technical Details

- Built using Dash and Dash Bootstrap Components
- Data sourced from CSV files used for symbol generation
- Utilizes Dash DataTable for interactive data display
- Implements dynamic styling based on the user's theme preference

## Adding as a Submodule

To add this repository as a submodule to your existing project, follow these steps:

1. Open a terminal and navigate to your project's root directory.
2. Run the following command to add the KiCAD Symbol Generator as a submodule:

   ```
   git submodule add https://github.com/ionutms/KiCAD_Symbol_Generator.git
   ```

3. Commit the changes to your project:

   ```
   git commit -m "Add KiCAD Symbol Generator as submodule"
   ```

4. Push the changes to your remote repository:

   ```
   git push origin main
   ```

To update the submodule in the future, use:

```
git submodule update --remote KiCAD_Symbol_Generator
```

To clone a project that includes this submodule, use:

```
git clone --recursive https://github.com/yourusername/your-project.git
```

Or, if you've already cloned the project without the `--recursive` flag:

```
git submodule init
git submodule update
```

## Removing the Submodule

If you need to remove the KiCAD Symbol Generator submodule from your project, follow these steps:

1. Run the `deinit` command to unregister the submodule:

   ```
   git submodule deinit -f KiCAD_Symbol_Generator
   ```

2. Remove the submodule from the Git cache:

   ```
   rm -rf .git/modules/KiCAD_Symbol_Generator
   ```

3. Remove the submodule from the working tree:

   ```
   git rm -f KiCAD_Symbol_Generator
   ```

4. Commit the changes:

   ```
   git commit -m "Removed KiCAD Symbol Generator submodule"
   ```

5. Push the changes to your remote repository:

   ```
   git push origin main
   ```

After completing these steps, the KiCAD Symbol Generator submodule will be completely removed from your project.