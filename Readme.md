# OLX.ua

This is one of the leading marketplaces all around the world. This repo is to show a way to scrape some data from that site.
```
This is only created for educational purposes and the data scraped is not used outside for any bussiness purposes.
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages.
Makefile is created for installing the necessary packages.

- Create a virtual environment
```bash
make create_venv
```
or
```bash
python -m venv ./env
```
- Activate venv
```bash
make venv
```
or
```bash
source env/Scripts/activate
```
- install necessary packages in the requirements.txt file
```bash
make packages
```
- Make sure chromedriver.exe is placed inside PATH

### Make some modifications to the program and run
```bash
python scrape_olx.py
```