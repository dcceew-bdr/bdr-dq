# Data Quality Assessment Framework (DQAF) Script

This script executes Data Quality Framework (DQAF) tests on RDF data provided in Turtle (.ttl) format.

## Installation

This project uses `uv` for dependency management. To install the required dependencies listed in `pyproject.toml`:

```bash
uv sync
```

Alternatively, if you prefer using `pip`, you might be able to install dependencies directly from `pyproject.toml` (requires a recent version of pip):

```bash
pip install .
```

## Usage

You can run the script using `uv` or directly with `python` if the dependencies are installed in your environment.

### Command Syntax

```bash
# Using uv
uv run python Convert/main.py [options] <filename>

# Using python directly
python Convert/main.py [options] <filename>
```

### Arguments

*   `filename`: (Required) The path to the input Turtle file (.ttl) to be assessed.

### Options

*   `--scope {Chunk,Dataset,BDR}`: (Required) Specify the scope of the assessment run.
    *   `Chunk`: Assess a single chunk of data.
    *   `Dataset`: Assess a complete dataset.
    *   `BDR`: Assess data according to Biodiversity Data Repository standards.
*   `-h`, `--help`: Show the help message and exit.

## Examples

**Run assessment using `uv`:**

```bash
uv run python Convert/main.py --scope Dataset path/to/your/my_data.ttl
```

**Run assessment directly with `python`:**

```bash
python Convert/main.py --scope Dataset path/to/your/my_data.ttl
```
_NB: ensure you have activated the virtual environment._

**Show help message:**

```bash
# Using uv
uv run python Convert/main.py -h

# Using python directly
python Convert/main.py -h
```

## Output

Upon successful execution, the script will:

1.  Log the assessments being run to standard output (STDOUT).
2.  Generate output files in the `Convert/output/` directory:
    *   A file containing the DQAF assessment results, potentially with compressed literals for efficiency.
    *   A metadata file describing the assessment run.
    *   If a new vocabulary mapping is generated (linking compression codes to assessment and result URIs), an RDF version of this mapping will also be created in the output directory.
