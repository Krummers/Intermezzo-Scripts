# Intermezzo Scripts
This repository contains various scripts for automating processes related to Intermezzos. Currently, there are two programs available:
* Patcher: Automatically installs an Intermezzo.
* Generator: Generates a second patch on top of the standard one of an Intermezz for customisation.

## Installation and Tutorial
1. Install [Python](https://www.python.org/downloads/) from the official website. Do not use any other method of installing.
2. Install the following modules with the command ```pip install MODULE``` in a console:
* [requests](https://pypi.org/project/requests/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [mwclient](https://pypi.org/project/mwclient/)
3. Install [7zip](https://www.7-zip.org/download.html) and add it to PATH. This can be done by adding the location where 7zip is installed under ```Environment Variables > User Variables > Path > Edit > New```. Save all screens once this is completed.
4. Install [Wiimms SZS Tools](https://szs.wiimm.de/) and check if it is added to PATH.

### Requirements

#### Patcher
* Python
* Modules
  * requests
* 7zip
* Wiimms SZS Tools

#### Generator
* Python
* Modules
  * requests
  * python-dotenv
  * mwclient
* 7zip

### Usage

#### Patcher
1. Download the ```Patcher``` folder from this repository.
2. Put your ISO/WBFS in this aforementioned folder.
3. Activate ```Intermezzo.py``` and follow the instructions.

#### Generator
1. Since an API key is required, usage of this script is not possible.
