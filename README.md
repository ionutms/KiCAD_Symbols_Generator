# KiCad Symbol Generator and Electronic Components Database

This project provides automated generation of KiCad symbols from CSV data and hosts an interactive web-based electronic components database. It supports multiple component types and includes comprehensive manufacturer-specific databases.

## Table of Contents
- [Project Description](#project-description)
- [Project Structure](#project-structure)
- [Submodule Management](#submodule-management)
- [Scripts Overview](#scripts-overview)
- [Web Application](#web-application)
- [CSV Format](#csv-format)
- [Component Generation](#component-generation)

## Project Description

The KiCad Symbol Generator project automates the creation of KiCad symbols from CSV data, providing a comprehensive solution for:

1. **Symbol Generation**: Automatically creates KiCad `.kicad_sym` files from CSV component databases
2. **Component Databases**: Hosts extensive databases of electronic components from various manufacturers
3. **Web Interface**: Provides an interactive dashboard with filtering, sorting, and visualization capabilities
4. **Multi-Manufacturer Support**: Includes components from NXP, Nexperia, Texas Instruments, Analog Devices, and others

The project supports a wide range of component types including resistors, capacitors, transistors, diodes, inductors, transformers, connectors, and switches.

## Project Structure

The project is organized into several key directories that serve different purposes:

```
KiCAD_Symbols_Generator/
├── app/                                                 # Web application source
│   ├── data/                                            # Component CSV files used by the web app
│   │   ├── UNITED_CAPACITORS_DATA_BASE.csv              # Capacitor database
│   │   ├── UNITED_RESISTORS_DATA_BASE.csv               # Resistor database
│   │   ├── UNITED_TRANSISTORS_DATA_BASE.csv             # Transistor database
│   │   ├── UNITED_DIODES_DATA_BASE.csv                  # Diode database
│   │   ├── UNITED_INDUCTORS_DATA_BASE.csv               # Inductor database
│   │   ├── UNITED_TRANSFORMERS_DATA_BASE.csv            # Transformer database
│   │   ├── UNITED_CONNECTORS_DATA_BASE.csv              # Connector database
│   │   ├── UNITED_TACTILE_SWITCHES_DATA_BASE.csv        # Tactile switch database
│   │   ├── UNITED_SLIDE_SWITCHES_DATA_BASE.csv          # Slide switch database
│   │   ├── UNITED_DIP_SWITCHES_DATA_BASE.csv            # DIP switch database
│   │   ├── UNITED_CRYSTALS_DATA_BASE.csv                # Crystal/oscillator database
│   │   ├── UNITED_COUPLED_INDUCTORS_DATA_BASE.csv       # Coupled inductor database
│   │   ├── UNITED_MECHANICAL_DATA_BASE.csv              # Mechanical components database
│   │   ├── UNITED_MODULES_DATA_BASE.csv                 # Module components database
│   │   ├── UNITED_MOUSE_BITES_DATA_BASE.csv             # Mouse bites database
│   │   ├── UNITED_SOLDER_JUMPERS.csv                    # Solder jumper database
│   │   ├── UNITED_TEST_POINTS.csv                       # Test point database
│   │   ├── UNITED_IC_NEXPERIA.csv                       # NEXPERIA IC database
│   │   ├── UNITED_IC_NXP.csv                            # NXP IC database
│   │   ├── UNITED_IC_TI.csv                             # Texas Instruments IC database
│   │   └── UNITED_IC_ADI.csv                            # Analog Devices IC database
│   ├── pages/                                           # Individual component database pages
│   │   ├── home_page.py                                 # Home page with analytics and navigation
│   │   ├── united_resistors_data_base_page.py           # Resistor database page
│   │   ├── united_capacitors_data_base_page.py          # Capacitor database page
│   │   ├── united_transistors_data_base_page.py         # Transistor database page
│   │   ├── united_diodes_data_base_page.py              # Diode database page
│   │   ├── united_inductors_data_base_page.py           # Inductor database page
│   │   ├── united_transformers_data_base_page.py        # Transformer database page
│   │   ├── united_connectors_data_base_page.py          # Connector database page
│   │   ├── united_tactile_switches_data_base_page.py    # Tactile switches page
│   │   ├── united_slide_switches_data_base_page.py      # Slide switches page
│   │   ├── united_dip_switches_data_base_page.py        # DIP switches page
│   │   ├── united_crystals_data_base_page.py            # Crystals database page
│   │   ├── united_coupled_inductors_data_base_page.py   # Coupled inductors page
│   │   ├── united_mechanical_data_base_page.py          # Mechanical components page
│   │   ├── united_modules_data_base_page.py             # Modules page
│   │   ├── united_mouse_bites_data_base_page.py         # Mouse bites page
│   │   ├── united_solder_jumpers_data_base_page.py      # Solder jumpers page
│   │   ├── united_test_points_data_base_page.py         # Test points page
│   │   ├── united_nexperia_data_base_page.py            # NEXPERIA IC page
│   │   ├── united_nxp_data_base_page.py                 # NXP IC page
│   │   ├── united_texas_instruments_data_base_page.py   # TI IC page
│   │   └── united_analog_devices_data_base_page.py      # ADI IC page
│   │   └── utils/                                       # UI component utilities
│   │       ├── dash_component_utils.py                  # Dash component utilities
│   │       └── style_utils.py                           # Styling utilities for Dash components
│   ├── symbols/                                         # Generated KiCad symbol files (web app use)
│   └── footprints/                                      # KiCad footprint files
├── scripts/                                             # Symbol generation scripts
│   ├── resistors/                                       # Resistor symbol generation
│   │   ├── symbol_resistor_generator.py                 # Main resistor symbol generator
│   │   ├── symbol_resistors_specs.py                    # Resistor-specific specifications
│   │   ├── mpn_resistor_generator.py                    # MPN-specific resistor generator
│   │   ├── footprint_resistor_generator.py              # Footprint generator
│   │   └── footprint_resistor_specs.py                  # Footprint specifications
│   ├── capacitors/                                      # Capacitor symbol generation
│   │   ├── symbol_capacitor_generator.py                # Main capacitor symbol generator
│   │   ├── symbol_capacitors_specs.py                   # Capacitor-specific specifications
│   │   └── mpn_capacitor_generator.py                   # MPN-specific capacitor generator
│   ├── transistors/                                     # Transistor symbol generation
│   │   ├── symbol_transistor_generator.py               # Main transistor generator
│   │   ├── symbol_transistors_specs.py                  # Transistor-specific specifications
│   │   └── mpn_transistor_generator.py                  # MPN-specific transistor generator
│   ├── diodes/                                          # Diode symbol generation
│   │   ├── symbol_diode_generator.py                    # Main diode symbol generator
│   │   ├── symbol_diodes_specs.py                       # Diode-specific specifications
│   │   └── mpn_diode_generator.py                       # MPN-specific diode generator
│   ├── inductors/                                       # Inductor symbol generation
│   │   ├── symbol_inductor_generator.py                 # Main inductor generator
│   │   ├── symbol_inductors_specs.py                    # Inductor-specific specifications
│   │   └── mpn_inductor_generator.py                    # MPN-specific inductor generator
│   ├── coupled_inductors/                               # Coupled inductor generation
│   │   ├── symbol_coupled_inductor_generator.py         # Coupled inductor generator
│   │   ├── symbol_coupled_inductors_specs.py            # Coupled inductor specs
│   │   └── mpn_coupled_inductor_generator.py            # MPN-specific generator
│   ├── transformers/                                    # Transformer symbol generation
│   │   ├── symbol_transformer_generator.py              # Main transformer generator
│   │   ├── symbol_transformers_specs.py                 # Transformer-specific specifications
│   │   └── mpn_transformer_generator.py                 # MPN-specific transformer generator
│   ├── connectors/                                      # Connector symbol generation
│   │   ├── symbol_connector_generator.py                # Main connector generator
│   │   ├── symbol_connectors_specs.py                   # Connector-specific specifications
│   │   └── mpn_connector_generator.py                   # MPN-specific connector generator
│   ├── crystals/                                        # Crystal symbol generation
│   │   ├── symbol_crystal_generator.py                  # Main crystal generator
│   │   ├── symbol_crystals_specs.py                     # Crystal-specific specifications
│   │   └── mpn_crystal_generator.py                     # MPN-specific crystal generator
│   ├── switches/                                        # Switch symbol generation (DIP, slide, tactile)
│   │   ├── symbol_switch_generator.py                   # Main switch generator
│   │   ├── symbol_switches_specs.py                     # Switch-specific specifications
│   │   └── mpn_switch_generator.py                      # MPN-specific switch generator
│   ├── mechanical/                                      # Mechanical component generation
│   │   ├── symbol_mechanical_generator.py               # Mechanical component generator
│   │   ├── symbol_mechanicals_specs.py                  # Mechanical-specific specifications
│   │   └── mpn_mechanical_generator.py                  # MPN-specific mechanical generator
│   └── utilities/                                       # Common script utilities
│       ├── symbol_utils.py                              # Core functionality for symbol generation
│       ├── file_handler_utilities.py                    # File handling utilities
│       ├── print_message_utilities.py                   # Console output utilities
│       └── footprint_utils.py                           # Footprint utilities
│   └── kicad_sym_extractor.py                           # CSV extraction from existing symbols
├── symbols/                                             # Generated KiCad symbol files (output)
│   ├── UNITED_CAPACITORS_DATA_BASE.kicad_sym            # Generated capacitor symbols
│   ├── UNITED_RESISTORS_DATA_BASE.kicad_sym             # Generated resistor symbols
│   ├── UNITED_TRANSISTORS_DATA_BASE.kicad_sym           # Generated transistor symbols
│   ├── UNITED_DIODES_DATA_BASE.kicad_sym                # Generated diode symbols
│   ├── UNITED_INDUCTORS_DATA_BASE.kicad_sym             # Generated inductor symbols
│   ├── UNITED_TRANSFORMERS_DATA_BASE.kicad_sym          # Generated transformer symbols
│   ├── UNITED_CONNECTORS_DATA_BASE.kicad_sym            # Generated connector symbols
│   ├── UNITED_TACTILE_SWITCHES_DATA_BASE.kicad_sym      # Generated tactile switch symbols
│   ├── UNITED_SLIDE_SWITCHES_DATA_BASE.kicad_sym        # Generated slide switch symbols
│   ├── UNITED_DIP_SWITCHES_DATA_BASE.kicad_sym          # Generated DIP switch symbols
│   ├── UNITED_CRYSTALS_DATA_BASE.kicad_sym              # Generated crystal symbols
│   ├── UNITED_COUPLED_INDUCTORS_DATA_BASE.kicad_sym     # Generated coupled inductor symbols
│   ├── UNITED_MECHANICAL_DATA_BASE.kicad_sym            # Generated mechanical symbols
│   ├── UNITED_MODULES_DATA_BASE.kicad_sym               # Generated module symbols
│   ├── UNITED_MOUSE_BITES_DATA_BASE.kicad_sym           # Generated mouse bites symbols
│   ├── UNITED_SOLDER_JUMPERS.kicad_sym                  # Generated solder jumper symbols
│   ├── UNITED_TEST_POINTS.kicad_sym                     # Generated test point symbols
│   ├── UNITED_IC_NEXPERIA.kicad_sym                     # Generated NEXPERIA IC symbols
│   ├── UNITED_IC_NXP.kicad_sym                          # Generated NXP IC symbols
│   ├── UNITED_IC_TI.kicad_sym                           # Generated TI IC symbols
│   └── UNITED_IC_ADI.kicad_sym                          # Generated ADI IC symbols
├── footprints/                                          # Generated KiCad footprint files (output)
├── series_kicad_sym/                                    # Series-specific symbol files
├── repo_traffic_data/                                   # Analytics data for web app
├── app.py                                               # Web application entry point
├── pyproject.toml                                       # Python project configuration
└── README.md                                            # This file
```

### Key Directories:
- **`app/`**: Contains the Dash web application that serves the component databases interactively
- **`scripts/`**: Contains Python scripts for symbol generation, organized by component type
- **`symbols/`**: Output directory containing generated .kicad_sym files ready for use in KiCad
- **`footprints/`**: Output directory for generated footprint files

## Submodule Management

### Adding as a Submodule
To add this repository as a submodule to your existing project:

1. Navigate to your project's root directory:
   ```bash
   cd /path/to/your/project
   ```

2. Add the KiCAD Symbol Generator as a submodule:
   ```bash
   git submodule add https://github.com/ionutms/KiCAD_Symbols_Generator.git
   ```

3. Commit the changes:
   ```bash
   git commit -m "Add KiCAD Symbol Generator as submodule"
   ```

4. Push to your remote repository:
   ```bash
   git push origin main
   ```

### Updating the Submodule
To update the submodule to the latest version:
```bash
git submodule update --remote KiCAD_Symbols_Generator
```

### Removing the Submodule
To remove the submodule from your project:

1. Deinitialize the submodule:
   ```bash
   git submodule deinit -f KiCAD_Symbols_Generator
   ```

2. Remove from Git cache:
   ```bash
   rm -rf .git/modules/KiCAD_Symbols_Generator
   ```

3. Remove from working tree:
   ```bash
   git rm -f KiCAD_Symbols_Generator
   ```

4. Commit the changes:
   ```bash
   git commit -m "Remove KiCAD Symbol Generator submodule"
   ```

### Cloning a Project with Submodules
To clone a project that includes this submodule:

```bash
git clone --recursive https://github.com/username/project.git
```

Or if you've already cloned without `--recursive`:
```bash
git submodule init
git submodule update
```

## Scripts Overview

The `scripts/` directory contains Python modules for generating KiCad symbols from CSV data. Each subdirectory focuses on a specific component type:

### Core Utilities (`scripts/utilities/`)
- `symbol_utils.py`: Core functionality for generating KiCad symbol syntax, including:
  - Symbol headers and properties
  - Graphical representations for various component types
  - Pin definitions with proper numbering and naming
  - Component-specific graphics (resistors, capacitors, transistors, etc.)
- `file_handler_utilities.py`: CSV reading/writing operations
- `print_message_utilities.py`: Console output handling

### Component-Specific Generators
Each component subdirectory includes:
- Generator script that reads CSV and creates `.kicad_sym` files
- Specification files for component-specific attributes
- Component-specific utilities

#### Key Component Types:
- **Resistors (`scripts/resistors/`)**: Standard resistors, thermistors with proper zigzag graphics
- **Capacitors (`scripts/capacitors/`)**: Standard and polarized capacitors with appropriate symbols
- **Transistors (`scripts/transistors/`)**: NPN/PNP BJTs and N/P-channel MOSFETs with detailed graphics
- **Diodes (`scripts/diodes/`)**: Rectifier, Schottky, Zener, TVS, and LED diodes
- **Inductors (`scripts/inductors/`)**: With coil symbol representations
- **Transformers (`scripts/transformers/`)**: With coupled inductors and polarity dots
- **Connectors (`scripts/connectors/`)**: Configurable pin count with rectangle graphics
- **Switches (`scripts/switches/`)**: DIP, slide, and tactile switches with actuator graphics

### Symbol Extraction (`scripts/kicad_sym_extractor.py`)
Converts existing `.kicad.sym` files back to CSV format for:
- Extracting properties from existing symbol libraries
- Converting between formats
- Updating databases with new components from existing libraries

## Web Application

The web application provides an interactive interface for browsing component databases:

- **Multi-Page Architecture**: Individual pages for each component type
- **Advanced Filtering**: Real-time filtering and sorting capabilities
- **Customizable Views**: Column visibility toggles and pagination
- **Value Distribution Graphs**: Visual representation of component values
- **Theme Support**: Light/dark mode switching
- **Manufacturer Organization**: Databases organized by manufacturer (NXP, Nexperia, TI, ADI, etc.)
- **Repository Analytics**: Clone and visitor statistics visualization

## CSV Format

Component data follows this standard format:

```csv
Symbol Name,Reference,Value,Footprint,Datasheet,Description,Manufacturer,MPN,Tolerance,Voltage Rating
```

Example:
```csv
Symbol Name,Reference,Value,Footprint,Datasheet,Description,Manufacturer,MPN,Tolerance,Voltage Rating
R_000001,R,10k,footprints:R_0402_1005Metric,https://example.com/datasheet.pdf,Thick Film Resistors - SMD 0402 10Kohms 1% AEC-Q200,Panasonic,ERJ-2RKF1002X,1 %,50 V
```

## Component Generation

The symbol generation process includes:

1. Reading CSV data from input files
2. Creating KiCad symbol syntax with proper headers
3. Generating component-specific graphics (e.g., resistor zigzags, transistor symbols)
4. Adding pin definitions with correct numbering and naming
5. Including component properties as KiCad fields
6. Outputting properly formatted `.kicad_sym` files

The generated symbols include:
- Standard KiCad symbol library format
- Component-specific graphical representations
- Proper pin definitions with names and numbers
- All properties from the CSV file as symbol fields
- Manufacturer-specific attributes where applicable