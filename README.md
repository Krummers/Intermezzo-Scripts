# Intermezzo Scripts
This repository contains various scripts for automating processes related to Intermezzi. Currently, there are two scripts available:
* Krummers-Generator: Prepares resources for Pulsar's mass import feature and edits the distribution afterwards.
* Wiimm-Patcher: Automatically installs an Intermezzo from Wiimm.
* Wiimm-Language-Generator: Generates a `patch2.tar`, which can be applied to an Intermezzo from Wiimm for customisation.

## Installation
1. Install [Python](https://www.python.org/downloads/) from the official website. Do not use any other method of installing.
2. Install the required modules with the command `pip install -r requirements.txt` in a console with the provided file.
3. Install [7zip](https://www.7-zip.org/download.html) and add it to PATH. This can be done by adding the location where 7zip is installed under `Environment Variables > User Variables > Path > Edit > New` for Windows. Save all screens once this is completed.
4. Install [Wiimms SZS Tools](https://szs.wiimm.de/) v2.39a or higher and check if it is added to PATH.
5. Download this repository and place it in your desired location.

## Usage

### Krummers-Generator
1. Open the `Intermezzo-Scripts/Krummers-Generator` folder from this repository.
2. Activate `main.py` and follow the instructions.

### Wiimm-Patcher
1. Open the `Intermezzo-Scripts/Wiimm-Patcher` folder from this repository.
2. Put your game image in this aforementioned folder.
3. Activate `Intermezzo.py` and follow the instructions.

### Wiimm-Language-Generator
1. Open the `Intermezzo-Scripts/Wiimm-Language-Generator` folder from this repository.
2. Activate `Generator.py` and follow the instructions.
