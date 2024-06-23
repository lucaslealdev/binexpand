# BIN and CUE File Padding Script

## Description

This project contains a Python script that pads a BIN file to occupy an entire CD and updates the corresponding CUE file. Additionally, it includes a registry (REG) file to add a context menu option in Windows to facilitate the use of the script.

## Features

- **Pad BIN File**: Pads a BIN file to occupy an entire CD by adding a dummy track.
- **Update CUE File**: Updates the CUE file with the information of the added dummy track.
- **Windows Context Menu**: Allows executing the script directly from the context menu on .CUE files.

## Requirements

- Python 3.x
- Windows

## Installation

1. **Download the files**:
    - Clone the repository or [download as zip](https://github.com/lucaslealdev/binexpand/archive/refs/heads/main.zip)

2. **Set up the Windows Context Menu**:
    - Place the `expand.py` script in the `C:\binexpand\` directory.
    - Run the `context_menu.reg` file to add the "Expand Disc" option to the context menu for .CUE files.

## Usage

### Via Command Line

1. Navigate to the script directory:
    ```sh
    cd path/to/the/script
    ```

2. Execute the script passing the path to the .CUE file:
    ```sh
    python expand.py path/to/the/file.cue
    ```

### Via Windows Context Menu

1. Right-click on a .CUE file.
2. Select the **"Expand Disc"** option.
