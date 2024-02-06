# BDR Data Quality Assessment Tool.

This repository contains a software tool that executes Data Quality (DQ) tests against [ABIS](https://linked.data.gov.au/def/abis) data and also documentation on the DQ Assessment Framework from which the tests are created.

## DQ Software

The DQ assessment tool is a Python package stored in the `dq/` directory of this repository.

### Installation

This Python package relies on Python 3.11+ and the dependencies given in the `pyproject.toml` file that should be installed using the [Poetry](https://python-poetry.org/) dependency manager or PIP.

Here are the major steps needed to start using this package:

1. Download/clone this repository somewhere
2. Install Python, if you haven't already got it
   1. 3.11+ needed
3. Install Poetry (from the link above) in your Python environment (or just use PIP)
4. Create a [Virtual Environment](https://docs.python.org/3/library/venv.html) just for this package
   1. some programming tools, like [PyCharm](https://www.jetbrains.com/pycharm/) have integrated support for this
5. Load this package's dependencies into the Virtual Environment
   1. Poetry: You usually just need to activate the Virtual Environment and then run the command line command `poetry update` or use a programming tool's UI to install all the dependencies in the `pyproject.toml` file
   2. PIP: `~$ pip install -r requirements.txt` or `~$ python -m pip install -r requirements.txt`

After installation, run the tests - next section - to ensure everything's working.

### Testing

This package uses the [pytest](https://pytest.org) Python testing framework for its internal testing. The test suite for this package is contained in the `tests/` directory of this repository and may be executed, after Python environment setup and package dependency and pytest installation, like this:

```bash
~$ pytest -W ignore tests
```

or, if you haven't made pytest executable, like this:

```bash
~$ python -m pytest -W ignore tests
```

You should then see all the tests run and, hopefully, pass. If they do, your copy of BDR DQ is ready for development!

### Use

To run this application, use Python on the command line or integrate this package into another Python application.

For Python on the command line, navigate to the root folder of this repository and run:

```bash
~$ python -m dq -h
```

This will print out the list of available commands.


## Assessment Framework documentation

Documentation on the Data Quality Assessment Framework which this tool test for is stored in the `doc/` directory of this repository. 

## License & Rights

This software and the other resources in this repository are licensed for reuse using the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license, a copy of the deed of which is held in the LICENSE file in this repository.

## Contact

These criteria are maintained by the BDR Team:

**BDR Team**  
Department of Climate Change, Energy and the Environment (DCCEEW)  
<bdr@dcceew.gov.au> . 