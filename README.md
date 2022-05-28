# ADB utilities 

Usefull scripts to operate on your phone with adb

Compatible with python3.10+

## Venv (Windows)

```
py -3.10 -m venv .venv
.venv\Scripts\activate.bat
python install --upgrade pip
```

## Install

```
pip install .
```

## Test

```
pip install -e .[testing]
pytest
```

## Usage

```
screenshot -h
screencast -h
```