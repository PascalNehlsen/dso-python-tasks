# PDF Metadata Cleaner

This repository contains a Python tool that cleans metadata from a specified PDF document and linearizes it for improved web performance. The original file is replaced with the cleaned version.

> **WARNING:**  
> This tool is intended for educational and authorized use only. Unauthorized editing and processing of PDF documents may violate copyright or other legal protections. Please ensure you have explicit permission to modify any PDF file you target.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Adjusting the Script](#adjusting-the-script)
  - [Running the Tool](#running-the-tool)
- [Output](#output)
- [Contact](#contact)

## Features

This tool offers the following features:

- **Clean Metadata**: Removes all metadata from the specified PDF file.
- **Display Metadata**: Outputs old and cleaned metadata in the console for comparison.

## Getting Started

### Prerequisites

Before running the script, make sure you have the following installed:

- **Python 3.7 or higher**
- Python libraries:
  - `pikepdf`
  - `exiftool`

You can install these dependencies using `pip`:

```shell
pip install pikepdf exiftool
```

### Installation

**Clone the Repository**:

```shell
git clone https://github.com/yourusername/pdf-metadata-cleaner.git
cd pdf-metadata-cleaner
```

## Usage

### Adjusting the Script

Before running the tool, open `remove-metadata.py` and change the path to the PDF file in the `clean_pdf` function to specify the file you want to edit. Make sure that the PDF file is in the same folder as the script.

### Running the Tool

Run the script with the following command in the command line:

```shell
python remove-metadata.py
```

## Output

The script will print the old and cleaned metadata in the console, allowing you to compare the changes. The original PDF file will be replaced by the cleaned version.

## Contact

- Pascal Nehlsen - [LinkedIn](https://www.linkedin.com/in/pascal-nehlsen) - [mail@pascal-nehlsen.de](mailto:mail@pascal-nehlsen.de)
- Project Link: [https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/remove-metadata](https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/remove-metadata)
