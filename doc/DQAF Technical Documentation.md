# Data Quality Assessment Framework (DQAF) Detailed User Guide

This comprehensive user guide provides an in-depth overview of the Data Quality Assessment Framework (DQAF), detailing the installation requirements, execution instructions, module functions, and testing procedures. Each function and parameter is explained to facilitate full understanding and practical use of the framework.

---


## DQAF Requirements - Step-by-Step Setup Guide

This detailed guide covers the installation and configuration steps required to set up the environment for using the Data Quality Assessment Framework (DQAF), with example commands and usage scenarios.

---

### 1. Python Environment

#### Step 1.1: Check Python Version

DQAF requires **Python 3.7 or later**. Ensure you have the correct version installed by running:

```bash
python3 --version
```

##### Expected Output:
If Python is correctly installed, you should see an output similar to:
```
Python 3.8.10
```

> **Note**: If Python 3.7+ is not installed, please download and install the latest version from [Python.org](https://www.python.org/downloads/).

#### Step 1.2: Create a Virtual Environment

To isolate DQAF’s dependencies, it’s advisable to set up a virtual environment. This helps to avoid conflicts with other packages installed on your system.

1. Create a new virtual environment in the current directory:
   ```bash
   python3 -m venv dqaf_env
   ```

2. Activate the virtual environment:
   - **On Windows**:
     ```bash
     dqaf_env\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source dqaf_env/bin/activate
     ```

3. Once activated, your terminal prompt should show the virtual environment name, e.g., `(dqaf_env)`, indicating that the environment is active.

### 2. Required Python Libraries

DQAF requires several Python libraries. Install them using the following command:

```bash
pip install numpy pandas rdflib openpyxl
```

#### Explanation of Each Library:
- **NumPy**: Provides support for large, multi-dimensional arrays and matrices, along with mathematical functions to operate on these arrays.
- **pandas**: A data manipulation library for handling and analyzing structured data.
- **rdflib**: A library for working with RDF data and SPARQL queries.
- **openpyxl**: Allows reading and writing Excel files in `.xlsx` format, used in DQAF for loading definitions and scoring matrices.

##### Example:
To verify the installation, you can import each library in Python:

```python
python3
```

Then, run:
```python
import numpy as np
import pandas as pd
import rdflib
import openpyxl

print("Libraries loaded successfully.")
```

If no error messages appear, the libraries are correctly installed.

### 3. Directory and File Structure

DQAF is structured across multiple modules, each with specific dependencies. Ensure all files are organized within the same project directory for smooth functionality.

**Required Files**:
The following files should be in your project directory:
- `vocab_manager.py`
- `app.py`
- `assess.py`
- `defined_namespaces.py`
- `query_processor.py`
- `report_analysis.py`
- `scoring_manager.py`
- `usecase_manager.py`

#### Example Directory Structure:
```plaintext
DQAF_Project/
├── __main__.py
├── vocab_manager.py
├── app.py
├── assess.py
├── defined_namespaces.py
├── query_processor.py
├── report_analysis.py
├── scoring_manager.py
└── usecase_manager.py
```

> **Tip**: Keep a separate directory for any additional files such as output reports or RDF data.

### 4. Running DQAF - Initial Setup Test

#### Step 4.1: Test the Initial Setup

To confirm that everything is set up correctly, run the `__main__.py` script:

```bash
python __main__.py
```

If all dependencies are correctly installed, the script should begin execution without errors. The console output will provide a log of the assessment steps as they are processed.

#### Example Output:
```plaintext
Starting Data Quality Assessment Framework (DQAF)...
Loading vocabularies...
Setting up assessment configurations...
Assessment successfully initialized.
Generating output report in Turtle (.ttl) format...
DQAF process completed successfully.
```

---

#### Troubleshooting Common Setup Issues

- **Library Not Found**: If you receive an error indicating a missing library, ensure the virtual environment is active and re-run:
  ```bash
  pip install numpy pandas rdflib openpyxl
  ```

- **File Not Found**: Double-check the directory structure to ensure all required files are present.

---


## DQAF - How to Run Guide

This guide provides detailed instructions on running the Data Quality Assessment Framework (DQAF) after completing the setup requirements. It includes step-by-step commands, usage examples, and explanations of expected outputs.

---

### 1. Initial Setup and Directory Navigation

1. **Open a Terminal or Command Prompt**.
2. **Navigate** to the directory containing your DQAF project files. This directory should contain all required files (e.g., `vocab_manager.py`, `app.py`, `assess.py`, `scoring_manager.py`, etc.).

   Example:
   ```bash
   cd path/to/DQAF_Project
   ```

> **Note**: Replace `path/to/DQAF_Project` with the actual path where you have stored the DQAF files.

### 2. Activate Virtual Environment
If you set up a virtual environment during installation, activate it to ensure dependencies are isolated.

- **On Windows**:
  ```bash
  dqaf_env\Scripts\activate
  ```
- **On macOS/Linux**:
  ```bash
  source dqaf_env/bin/activate
  ```

Your terminal prompt should now indicate that the virtual environment is active.

### 3. Running the Main Script

To start the DQAF, run the main script (`__main__.py`). This script initializes the application and performs data quality assessments based on the configuration and input data.

```bash
python __main__.py
```

This command triggers the framework to load data files, execute quality checks, and generate output files.

#### Example Console Output:
You should see output similar to the following:
```plaintext
Starting Data Quality Assessment Framework (DQAF)...
Loading vocabularies...
Setting up assessment configurations...
Assessment successfully initialized.
Performing data quality checks...
Scoring and use case assessments in progress...
Generating output report in Turtle (.ttl) format...
DQAF process completed successfully.
```

---

### 4. Interpreting Output and Reports

After running the main script, DQAF generates an output report detailing the quality assessment. By default, this report is saved in Turtle (`.ttl`) format within the output directory.

- **Output Location**: The report location is configured in `app.py`. Check this file if you need to confirm or modify the output path.

- **Example Output File**: 
   ```plaintext
   DQAF_Project/output/assessment_report.ttl
   ```

#### Key Sections in the Output Report:
The `.ttl` report includes the following main sections:

1. **Assessment Summaries**: Overview of the data quality scores across various metrics.
2. **Scoring Details**: Detailed results for each scoring method applied.
3. **Use Case Evaluations**: Evaluations of data quality based on specific use cases defined by the user.

---

### 5. Running Tests and Debugging

To validate the functionality or troubleshoot any issues, consider the following:

#### Testing the Script

Re-run `__main__.py` with test data to confirm functionality. Errors or warnings during execution may point to data inconsistencies or configuration issues.

#### Console Output Logs

- **Error Messages**: Console output will provide any error messages, usually identifying the file or function causing issues.
- **Debugging Tips**:
  - Check for missing dependencies or invalid paths.
  - Verify that input data files are in the expected format and location.

---

### 6. Modifying Configurations and Re-running

To customize the assessment:

1. **Edit Configuration Files**: Modify parameters in `app.py` or other configuration files to adjust paths, scoring criteria, or use case definitions.
2. **Re-run the Script**:
   ```bash
   python __main__.py
   ```

Changes will take effect based on your new configurations.

---

### 7. Example Workflow

#### Step 1: Run DQAF with Sample Data
```bash
python __main__.py
```

#### Step 2: Review Output in `.ttl` Format
Navigate to the output directory and open the report file to view assessment results.

---

For further details or troubleshooting, please refer to the DQAF documentation or contact the support team.


## DQAF - `vocab_manager.py` Guide

This guide focuses on the `vocab_manager.py` module in the Data Quality Assessment Framework (DQAF). The `vocab_manager.py` file is responsible for managing vocabularies used in assessments, ensuring consistent use of terms and validating entries across the framework.

---

### Overview of `VocabManager` Class

The `VocabManager` class in `vocab_manager.py` provides methods for loading, managing, and validating vocabularies. It plays a critical role in the framework by handling predefined vocabulary lists that other components rely on for assessments.

#### Key Functions in `VocabManager`

Each function in `VocabManager` is designed to facilitate a specific aspect of vocabulary handling, from loading vocab data to validating terms and ensuring consistency.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self):
    pass
```

**Description**:
The `__init__` method initializes the `VocabManager` instance. While this method does not load data itself, it sets up the object for later vocabulary operations, including loading and validation.

#### 2. `load_vocab`

**Syntax**:
```python
def load_vocab(self, vocab_file_path):
    pass
```

**Parameters**:
- `vocab_file_path` (str): The path to the file containing vocabulary data. This file is expected to have specific terms and definitions used in the DQAF assessments.

**Description**:
The `load_vocab` function loads vocabulary data from the specified file path. The function reads vocabulary definitions and mappings, storing them within the `VocabManager` object. This vocabulary list is later referenced by other modules for data quality assessments.

**Example**:
```python
vocab_manager = VocabManager()
vocab_manager.load_vocab("path/to/vocab_file.csv")
```

#### 3. `validate_vocab`

**Syntax**:
```python
def validate_vocab(self, terms_to_validate):
    pass
```

**Parameters**:
- `terms_to_validate` (list): A list of terms that need to be validated against the loaded vocabulary.

**Description**:
The `validate_vocab` function checks each term in `terms_to_validate` against the vocabulary data that was loaded with `load_vocab`. If any term does not exist in the loaded vocabulary, it is flagged as an inconsistency, which can help maintain data quality.

**Example**:
```python
vocab_manager = VocabManager()
vocab_manager.load_vocab("path/to/vocab_file.csv")
invalid_terms = vocab_manager.validate_vocab(["term1", "term2", "term3"])
if invalid_terms:
    print("Invalid terms found:", invalid_terms)
else:
    print("All terms are valid.")
```

---

### Example Workflow

Below is an example workflow demonstrating how to use the `VocabManager` class to load and validate vocabulary:

#### Step 1: Initialize and Load Vocabulary

1. Import and initialize `VocabManager`:
    ```python
    from vocab_manager import VocabManager
    vocab_manager = VocabManager()
    ```

2. Load the vocabulary data:
    ```python
    vocab_manager.load_vocab("path/to/vocab_file.csv")
    ```

#### Step 2: Validate Terms

1. Define the terms to validate and run validation:
    ```python
    terms_to_validate = ["termA", "termB", "termC"]
    invalid_terms = vocab_manager.validate_vocab(terms_to_validate)
    ```

2. Check the results:
    ```python
    if invalid_terms:
        print("The following terms are invalid:", invalid_terms)
    else:
        print("All terms are valid.")
    ```

---

### Additional Notes

- **Vocabulary File Format**: Ensure that the vocabulary file (e.g., `.csv` or `.txt`) is formatted according to expected standards. Each row should represent a valid term for the framework.
- **Error Handling**: If an invalid file path or an incorrectly formatted file is provided, the `load_vocab` function will raise an error. Ensure correct paths and file structure.

This concludes the guide for `vocab_manager.py` in DQAF. For further assistance, refer to the DQAF documentation or contact support.


## DQAF - `app.py` Guide

This guide focuses on the `app.py` module in the Data Quality Assessment Framework (DQAF). The `app.py` file serves as the central controller of the application, setting up configurations, initializing key components, and managing the overall flow of the assessment process.

---

### Overview of the `App` Class

The `App` class in `app.py` is responsible for orchestrating the entire DQAF process, from loading configurations to executing assessments. It brings together the different components of the framework, such as vocabulary management and scoring, to ensure that assessments are conducted accurately.

#### Key Functions in the `App` Class

Each function in the `App` class plays a specific role in managing the flow of data and execution. This guide provides details on these functions to help you understand their purpose and usage.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self):
    pass
```

**Description**:
The `__init__` function initializes an instance of the `App` class, setting up any essential configurations or paths required for DQAF to run. This function prepares the application for further setup and execution by instantiating necessary components.

---

#### 2. `setup_assessment`

**Syntax**:
```python
def setup_assessment(self, config_file_path):
    pass
```

**Parameters**:
- `config_file_path` (str): Path to the configuration file that contains settings for the assessment. This file typically defines paths, thresholds, and parameters needed for data quality assessments.

**Description**:
The `setup_assessment` function loads and applies configuration settings from the provided file. These settings include the paths for input data, report output location, and parameters for scoring and use cases. This function is critical for ensuring that DQAF is tailored to the specific requirements of each assessment.

**Example**:
```python
app = App()
app.setup_assessment("path/to/config_file.json")
```

> **Note**: Ensure the configuration file follows the correct format (e.g., JSON) with required fields specified.

---

#### 3. `run_assessment`

**Syntax**:
```python
def run_assessment(self):
    pass
```

**Description**:
The `run_assessment` function is the main function that orchestrates the execution of the assessment. It coordinates the interaction between different modules (e.g., vocabulary manager, scoring manager) to perform the full assessment, from data quality checks to scoring and report generation.

This function performs the following steps:
1. Initializes data quality checks.
2. Runs scoring methods on the data.
3. Collects results and generates a report in the specified output format (e.g., Turtle `.ttl` file).

**Example**:
```python
app = App()
app.setup_assessment("path/to/config_file.json")
app.run_assessment()
```

After `run_assessment` completes, an output file with the assessment results is generated in the specified directory.

---

### Example Workflow

Below is an example workflow demonstrating how to use the `App` class to set up and execute an assessment.

#### Step 1: Initialize the `App` Class

1. Import and initialize an instance of `App`:
    ```python
    from app import App
    app = App()
    ```

#### Step 2: Configure the Assessment

1. Set up the assessment using a configuration file. This configuration file defines all the necessary paths and parameters.
    ```python
    app.setup_assessment("path/to/config_file.json")
    ```

#### Step 3: Run the Assessment

1. Execute the assessment:
    ```python
    app.run_assessment()
    ```

2. Once complete, check the output directory for the assessment report.

---

### Additional Notes

- **Configuration File Format**: Ensure the configuration file includes all required settings, such as paths to input data and output directories, and any thresholds for scoring.
- **Error Handling**: The `run_assessment` function will output errors to the console if required files are missing or misconfigured. Ensure paths and file formats are correct before running.

This concludes the guide for `app.py` in DQAF. For further assistance, refer to additional documentation or contact support.


## DQAF - `assess.py` Guide

This guide provides a detailed overview of the `assess.py` module in the Data Quality Assessment Framework (DQAF). The `assess.py` file is responsible for managing data quality assessments and includes functions for evaluating key metrics, such as date recency and datum validation.

---

### Overview of the `AssessmentManager` Class

The `AssessmentManager` class in `assess.py` handles the core assessments within DQAF. This class provides methods to validate data integrity, calculate quality scores, and assess criteria like date recency and location precision.

#### Key Functions in `AssessmentManager`

Each function in `AssessmentManager` evaluates a specific data quality metric or performs related validation. This guide provides details on these functions to facilitate understanding of their purpose and usage.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self, data_file):
    pass
```

**Parameters**:
- `data_file` (str): Path to the data file that will be assessed.

**Description**:
The `__init__` method initializes the `AssessmentManager` instance by loading the data file specified in the parameter. It prepares the class for performing assessments on this data.

**Example**:
```python
assessment_manager = AssessmentManager("path/to/data_file.csv")
```

---

#### 2. `validate_data`

**Syntax**:
```python
def validate_data(self):
    pass
```

**Description**:
The `validate_data` function checks the input data for structural validity. It ensures that required columns and data formats are present and correct, which is essential for accurate quality assessments.

**Example**:
```python
assessment_manager = AssessmentManager("path/to/data_file.csv")
is_valid = assessment_manager.validate_data()
if is_valid:
    print("Data is valid.")
else:
    print("Data validation failed.")
```

---

#### 3. `calculate_scores`

**Syntax**:
```python
def calculate_scores(self):
    pass
```

**Description**:
The `calculate_scores` function calculates data quality scores based on multiple metrics. Each score represents the data quality level in a specific area, such as completeness or precision. This function aggregates scores to provide an overall data quality rating.

**Example**:
```python
assessment_manager.calculate_scores()
print("Scores calculated successfully.")
```

---

#### 4. `date_recency_datum_validation`

**Syntax**:
```python
def date_recency_datum_validation(self, date_column, threshold_date):
    pass
```

**Parameters**:
- `date_column` (str): The name of the column containing date information in the dataset.
- `threshold_date` (str or datetime): The reference date used to determine if data is recent. Data older than this date may be flagged.

**Description**:
The `date_recency_datum_validation` function assesses whether dates in the specified column are recent compared to the threshold date. Records with dates older than the threshold are marked as outdated, affecting the overall quality score for date recency.

**Example**:
```python
from datetime import datetime

threshold = datetime(2020, 1, 1)
is_recent = assessment_manager.date_recency_datum_validation("observation_date", threshold)
if is_recent:
    print("Date recency validation passed.")
else:
    print("Some records are outdated.")
```

---

#### 5. `location_precision`

**Syntax**:
```python
def location_precision(self, lat_column, lon_column, precision_threshold):
    pass
```

**Parameters**:
- `lat_column` (str): The column name for latitude values.
- `lon_column` (str): The column name for longitude values.
- `precision_threshold` (float): A threshold value defining acceptable precision for location data.

**Description**:
The `location_precision` function evaluates the accuracy of geographic coordinates in the data. Records with precision below the threshold are flagged, which can affect the data quality score for location precision.

**Example**:
```python
precision_threshold = 0.01
location_valid = assessment_manager.location_precision("latitude", "longitude", precision_threshold)
if location_valid:
    print("Location precision validation passed.")
else:
    print("Some records have low location precision.")
```

---

### Example Workflow

Below is an example workflow demonstrating how to use the `AssessmentManager` class to set up and execute data quality assessments.

#### Step 1: Initialize the `AssessmentManager` Class

1. Import and initialize an instance of `AssessmentManager`:
    ```python
    from assess import AssessmentManager
    assessment_manager = AssessmentManager("path/to/data_file.csv")
    ```

#### Step 2: Validate Data

1. Run the data validation check:
    ```python
    is_valid = assessment_manager.validate_data()
    if is_valid:
        print("Data is valid.")
    else:
        print("Data validation failed.")
    ```

#### Step 3: Run Assessments

1. Calculate data quality scores based on various metrics:
    ```python
    assessment_manager.calculate_scores()
    ```

2. Check date recency for data:
    ```python
    from datetime import datetime
    threshold_date = datetime(2021, 1, 1)
    is_recent = assessment_manager.date_recency_datum_validation("observation_date", threshold_date)
    ```

3. Evaluate location precision:
    ```python
    precision_valid = assessment_manager.location_precision("latitude", "longitude", 0.01)
    ```

---

### Additional Notes

- **Data File Format**: Ensure the data file (e.g., `.csv`) contains all required columns in the correct format. Each column should have values compatible with the expected data types for each function (e.g., date, latitude/longitude).
- **Error Handling**: Functions like `validate_data` return validation results. Check these before proceeding with further assessments.

This concludes the guide for `assess.py` in DQAF. For additional information, refer to the full documentation or contact support.


## DQAF - `defined_namespaces.py` Guide

This guide provides an overview of the `defined_namespaces.py` module in the Data Quality Assessment Framework (DQAF). This module is crucial for defining consistent namespace URIs used throughout the framework, which are essential for ensuring standardization in data quality assessments.

---

### Purpose of `defined_namespaces.py`

The `defined_namespaces.py` module contains a set of predefined namespaces used across the DQAF to ensure data is interpreted uniformly. By assigning each concept to a unique URI, namespaces provide a foundation for interoperability and data quality standardization.

#### Key Namespaces Defined

The following namespaces are specified in `defined_namespaces.py`, each with a distinct URI. These namespaces cover concepts relevant to data quality, biodiversity, and environmental research.

#### 1. DQAF - Data Quality Assessment Framework Namespace

**Namespace URI**: `https://example.com/def/dqaf/`

**Description**:
The `DQAF` namespace defines the core terms and predicates used within the Data Quality Assessment Framework. This namespace is used for all terms specifically created for or tailored to the needs of the DQAF.

**Example Use**:
```python
from defined_namespaces import DQAF
print(DQAF.hasDQAFResult)  # URIRef for a specific DQAF property
```

#### 2. BDRM - Biodiversity Message Namespace

**Namespace URI**: `https://linked.data.gov.au/def/bdr-msg/`

**Description**:
The `BDRM` namespace defines terms used in biodiversity messaging and data sharing within Australian government-linked data projects. This namespace supports fields related to biodiversity assessments and species observation data.

**Example Use**:
```python
from defined_namespaces import BDRM
print(BDRM.speciesObserved)  # URIRef for a biodiversity-related term
```

#### 3. DWC - Darwin Core Namespace

**Namespace URI**: `http://rs.tdwg.org/dwc/terms/`

**Description**:
The `DWC` (Darwin Core) namespace is a standardized schema used for biodiversity data, primarily focused on sharing data about biological collections. Terms within the Darwin Core vocabulary are used by DQAF to map species and environmental data to standardized fields.

**Example Use**:
```python
from defined_namespaces import DWC
print(DWC.occurrenceID)  # URIRef for Darwin Core's occurrence ID term
```

#### 4. TERN - Terrestrial Ecosystem Research Network Namespace

**Namespace URI**: `https://w3id.org/tern/ontologies/tern/`

**Description**:
The `TERN` namespace supports terms related to terrestrial ecosystems and environmental research in Australia. This namespace helps in mapping DQAF data related to ecosystems to TERN standards, enabling broader use in environmental assessments.

**Example Use**:
```python
from defined_namespaces import TERN
print(TERN.siteID)  # URIRef for TERN's site ID term
```

---

### Example Workflow Using Namespaces

Below is an example demonstrating how to use these namespaces in a DQAF-based script to build RDF triples.

#### Step 1: Import Required Namespaces

1. Import the required namespaces from `defined_namespaces.py`:
    ```python
    from rdflib import Graph, URIRef, Literal
    from defined_namespaces import DQAF, BDRM, DWC, TERN
    ```

#### Step 2: Create RDF Triples Using Namespaces

1. Initialize an RDF graph:
    ```python
    g = Graph()
    ```

2. Use namespaces to define triples:
    ```python
    subject = URIRef("http://example.com/observation/12345")
    g.add((subject, DQAF.hasDQAFResult, Literal("High Quality")))
    g.add((subject, BDRM.speciesObserved, Literal("Eucalyptus")))
    g.add((subject, DWC.occurrenceID, Literal("Occ12345")))
    g.add((subject, TERN.siteID, Literal("Site67890")))
    ```

3. Serialize the graph to view the output:
    ```python
    print(g.serialize(format="turtle").decode("utf-8"))
    ```

---

### Additional Notes

- **URIRef Usage**: All namespaces are imported as `URIRef` objects, allowing them to be directly used in RDF triples.
- **Namespace Consistency**: Using predefined namespaces ensures consistent interpretation of data fields across different modules and applications.

This concludes the guide for `defined_namespaces.py` in DQAF. For further support, refer to the DQAF documentation or contact the support team.


## DQAF - `query_processor.py` Guide

This guide provides an in-depth look at the `query_processor.py` module in the Data Quality Assessment Framework (DQAF). This module is essential for processing SPARQL queries on RDF data, enabling targeted assessments and data extraction based on user-defined criteria.

---

### Overview of `RDFQueryProcessor` Class

The `RDFQueryProcessor` class in `query_processor.py` is designed to execute and manage SPARQL queries on RDF graphs. This class loads RDF data and provides functions to run customized queries, making it easier to filter and retrieve specific information from datasets.

#### Key Functions in `RDFQueryProcessor`

Each function in `RDFQueryProcessor` is designed to facilitate a specific aspect of RDF query processing, from initializing the RDF graph to executing queries and printing results.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self, filepath, format="turtle"):
    pass
```

**Parameters**:
- `filepath` (str): The path to the RDF file that contains the data to be queried.
- `format` (str): The format of the RDF file (default is `"turtle"`). Supported formats include Turtle (`.ttl`), RDF/XML (`.rdf`), N-Triples (`.nt`), and more.

**Description**:
The `__init__` method initializes the RDF graph by loading data from the specified file. It prepares the `RDFQueryProcessor` to execute SPARQL queries on the loaded graph.

**Example**:
```python
query_processor = RDFQueryProcessor("path/to/rdf_data.ttl", format="turtle")
```

> **Note**: Ensure the RDF file is correctly formatted; otherwise, parsing errors may occur.

---

#### 2. `execute_query`

**Syntax**:
```python
def execute_query(self, out_p_uri, aus_st_uri, out_p_value="normal", aus_st_value="Western_Australia"):
    pass
```

**Parameters**:
- `out_p_uri` (str): The URI for the output property to filter within the query.
- `aus_st_uri` (str): The URI for the Australian state property in the query.
- `out_p_value` (str): The expected value for the output property (default is `"normal"`).
- `aus_st_value` (str): The expected value for the Australian state (default is `"Western_Australia"`).

**Description**:
The `execute_query` function forms and executes a SPARQL query on the RDF graph using the provided parameters. It is designed to filter data based on specified properties and their values, making it useful for targeted queries.

**Example**:
```python
results = query_processor.execute_query(
    out_p_uri="http://example.com/ontology/outputProperty",
    aus_st_uri="http://example.com/ontology/australianState",
    out_p_value="normal",
    aus_st_value="Western_Australia"
)
```

The function returns results matching the specified criteria.

---

#### 3. `print_results`

**Syntax**:
```python
def print_results(self, results):
    pass
```

**Parameters**:
- `results`: A collection of results obtained from a SPARQL query execution.

**Description**:
The `print_results` function outputs the query results to the console. It iterates over each result in the collection, displaying relevant information. This function is useful for quick, interactive inspection of query outcomes.

**Example**:
```python
results = query_processor.execute_query(
    out_p_uri="http://example.com/ontology/outputProperty",
    aus_st_uri="http://example.com/ontology/australianState"
)
query_processor.print_results(results)
```

---

### Example Workflow

Below is an example workflow demonstrating how to use the `RDFQueryProcessor` class to load RDF data, execute a query, and print the results.

#### Step 1: Initialize the `RDFQueryProcessor` Class

1. Import and initialize an instance of `RDFQueryProcessor`:
    ```python
    from query_processor import RDFQueryProcessor
    query_processor = RDFQueryProcessor("path/to/rdf_data.ttl", format="turtle")
    ```

#### Step 2: Execute a Query

1. Define query parameters and execute the query:
    ```python
    results = query_processor.execute_query(
        out_p_uri="http://example.com/ontology/outputProperty",
        aus_st_uri="http://example.com/ontology/australianState",
        out_p_value="normal",
        aus_st_value="Western_Australia"
    )
    ```

#### Step 3: Print Query Results

1. Display the results using the `print_results` function:
    ```python
    query_processor.print_results(results)
    ```

This sequence will load the RDF data, perform a query based on specified URIs and values, and print the matched results.

---

### Additional Notes

- **SPARQL Query Customization**: Modify the `execute_query` function parameters to filter based on different properties and values.
- **Supported Formats**: The RDF graph format (default `"turtle"`) can be changed to accommodate other formats such as `"rdf/xml"` or `"ntriples"`.
- **Error Handling**: If parsing errors occur, verify the RDF file format and structure.

This concludes the guide for `query_processor.py` in DQAF. For further assistance, refer to the full DQAF documentation or contact support.


## DQAF - `report_analysis.py` Guide

This guide provides an in-depth overview of the `report_analysis.py` module in the Data Quality Assessment Framework (DQAF). This module is essential for analyzing RDF reports, summarizing namespace frequencies, evaluating unique predicates, and assessing data quality metrics.

---

### Overview of the `ReportAnalysis` Class

The `ReportAnalysis` class in `report_analysis.py` processes RDF data, analyzing namespaces, predicates, and other metrics relevant to data quality. This class is critical for generating quality insights and compiling reports.

#### Key Functions in `ReportAnalysis`

Each function in `ReportAnalysis` performs a specific type of analysis on the RDF data. Below is a breakdown of each function, including its purpose, parameters, and usage examples.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self, g, report_file=None):
    pass
```

**Parameters**:
- `g` (rdflib.Graph): The RDF graph object containing the data to be analyzed.
- `report_file` (file object, optional): A file object where the report will be written if provided.

**Description**:
The `__init__` method initializes an instance of `ReportAnalysis`, setting up the RDF graph for analysis and preparing the report output location.

**Example**:
```python
from rdflib import Graph
rdf_graph = Graph().parse("path/to/rdf_data.ttl", format="turtle")
report_analysis = ReportAnalysis(rdf_graph, report_file=open("report.txt", "w"))
```

---

#### 2. `namespace_frequencies`

**Syntax**:
```python
def namespace_frequencies(self):
    pass
```

**Description**:
The `namespace_frequencies` function calculates the frequency of each namespace within the RDF graph. This provides insights into the distribution and usage of different namespaces, which can highlight inconsistencies or unexpected patterns.

**Example**:
```python
frequencies = report_analysis.namespace_frequencies()
for namespace, count in frequencies:
    print(f"{namespace}: {count}")
```

---

#### 3. `get_sorted_namespaces`

**Syntax**:
```python
def get_sorted_namespaces(self):
    pass
```

**Description**:
The `get_sorted_namespaces` function retrieves namespaces sorted by frequency. It returns a list of tuples, each containing the prefix, URI, and count of appearances. This provides a structured view of namespace usage in the data.

**Example**:
```python
sorted_namespaces = report_analysis.get_sorted_namespaces()
for prefix, uri, count in sorted_namespaces:
    print(f"{prefix if prefix else 'No Prefix'} - {uri}: {count}")
```

---

#### 4. `analyze_unique_predicates`

**Syntax**:
```python
def analyze_unique_predicates(self):
    pass
```

**Description**:
The `analyze_unique_predicates` function calculates the frequency of unique predicates in the RDF data, providing a dictionary where keys are predicates, and values are their respective counts. This is useful for understanding the variety and usage of predicates in the dataset.

**Example**:
```python
predicate_counts = report_analysis.analyze_unique_predicates()
for predicate, count in predicate_counts.items():
    print(f"{predicate}: {count}")
```

---

#### 5. `predicate_value_assessment`

**Syntax**:
```python
def predicate_value_assessment(self):
    pass
```

**Description**:
The `predicate_value_assessment` function evaluates the completeness of predicate values in the RDF data. It returns a dictionary indicating whether each predicate has empty or non-empty values, which helps assess data completeness.

**Example**:
```python
value_assessment = report_analysis.predicate_value_assessment()
for predicate, values in value_assessment.items():
    print(f"{predicate} - Non-empty: {values['non_empty']}, Empty: {values['empty']}")
```

---

#### 6. `generate_report`

**Syntax**:
```python
def generate_report(self):
    pass
```

**Description**:
The `generate_report` function compiles a comprehensive data quality assessment report. It includes a summary of triples, unique predicates, namespaces, and other relevant metrics, and writes these results to the specified report file.

**Example**:
```python
report_analysis.generate_report()
print("Report generated successfully.")
```

---

#### 7. `calculate_predicate_completeness`

**Syntax**:
```python
def calculate_predicate_completeness(self, predicate_uri):
    pass
```

**Parameters**:
- `predicate_uri` (str or rdflib.URIRef): The URI of the predicate to assess.

**Description**:
The `calculate_predicate_completeness` function calculates the completeness of a specific predicate by checking the presence of values for that predicate across relevant subjects. It returns a score representing the completeness level.

**Example**:
```python
completeness_score = report_analysis.calculate_predicate_completeness("http://example.com/predicate")
print(f"Predicate completeness: {completeness_score}")
```

---

### Example Workflow Using `ReportAnalysis`

Below is an example workflow demonstrating how to use the `ReportAnalysis` class to analyze RDF data and generate a report.

#### Step 1: Initialize the `ReportAnalysis` Class

1. Import and initialize an RDF graph and instance of `ReportAnalysis`:
    ```python
    from rdflib import Graph
    from report_analysis import ReportAnalysis
    
    rdf_graph = Graph().parse("path/to/rdf_data.ttl", format="turtle")
    report_file = open("assessment_report.txt", "w")
    report_analysis = ReportAnalysis(rdf_graph, report_file)
    ```

#### Step 2: Run Analysis Functions

1. Generate namespace frequencies:
    ```python
    print(report_analysis.namespace_frequencies())
    ```

2. Retrieve sorted namespaces:
    ```python
    print(report_analysis.get_sorted_namespaces())
    ```

3. Analyze unique predicates:
    ```python
    print(report_analysis.analyze_unique_predicates())
    ```

4. Assess predicate values:
    ```python
    print(report_analysis.predicate_value_assessment())
    ```

#### Step 3: Generate the Final Report

1. Create a complete data quality assessment report:
    ```python
    report_analysis.generate_report()
    report_file.close()
    ```

This sequence analyzes the RDF data, compiles various metrics, and writes the results to a report file.

---

### Additional Notes

- **Output Format**: The `generate_report` function writes the analysis results to the specified report file. Check this file for a summary of data quality metrics.
- **Error Handling**: If errors occur, ensure that the RDF data file is valid and the necessary libraries are installed.

This concludes the guide for `report_analysis.py` in DQAF. For further assistance, refer to the DQAF documentation or contact support.


## DQAF - `scoring_manager.py` Guide

This guide provides a detailed overview of the `scoring_manager.py` module in the Data Quality Assessment Framework (DQAF). This module is responsible for applying scoring methods to assess data quality based on pre-defined criteria, with functions to calculate, store, and report scores.

---

### Overview of the `ScoringManager` Class

The `ScoringManager` class in `scoring_manager.py` manages the entire scoring process, from loading scoring definitions to applying scoring methods on the data. This class is essential for quantifying data quality based on specific metrics, generating scores that contribute to the overall quality assessment.

#### Key Functions in `ScoringManager`

Each function in `ScoringManager` facilitates a unique aspect of scoring, from creating scoring matrices to calculating and storing scores. Below is a breakdown of each function, its purpose, parameters, and usage.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self, scoring_definition_excel_file, assess_matrix_df, results_ttl, output_result_file, report_file=None):
    pass
```

**Parameters**:
- `scoring_definition_excel_file` (str): Path to the Excel file containing scoring definitions.
- `assess_matrix_df` (pd.DataFrame): DataFrame holding assessment data for scoring.
- `results_ttl` (str): Path to the Turtle file with existing results to load.
- `output_result_file` (str): File path for saving the output results in Turtle format.
- `report_file` (file object, optional): File object for writing the scoring report.

**Description**:
The `__init__` method initializes the `ScoringManager`, loading scoring definitions, setting up data matrices, and preparing files for output.

**Example**:
```python
scoring_manager = ScoringManager("scoring_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
```

---

#### 2. `create_scoring_matrix`

**Syntax**:
```python
def create_scoring_matrix(self):
    pass
```

**Description**:
The `create_scoring_matrix` function loads scoring definitions from the specified Excel file and organizes them into a scoring matrix. This matrix forms the basis of the scoring assessments, detailing weightings and criteria for each score.

**Example**:
```python
scoring_manager.create_scoring_matrix()
print("Scoring matrix created successfully.")
```

---

#### 3. `apply_scoring_methods`

**Syntax**:
```python
def apply_scoring_methods(self):
    pass
```

**Description**:
The `apply_scoring_methods` function iterates through the assessment matrix and applies each scoring method from the scoring matrix to the data. It calculates scores based on the predefined criteria and writes these scores to the results file.

**Example**:
```python
scoring_manager.apply_scoring_methods()
print("Scoring methods applied successfully.")
```

---

#### 4. `_add_scoring_result`

**Syntax**:
```python
def _add_scoring_result(self, scoring_method, observation_id, value, scoring_date=None):
    pass
```

**Parameters**:
- `scoring_method` (str): The name of the scoring method being applied.
- `observation_id` (str or int): The unique identifier of the observation being scored.
- `value` (float): The calculated score for the observation.
- `scoring_date` (datetime, optional): The date of scoring. Defaults to the current date.

**Description**:
The `_add_scoring_result` function creates a new RDF triple for each scoring result and adds it to the RDF graph. This function helps store each score in a structured format, enabling consistent reporting and retrieval.

**Example**:
```python
scoring_manager._add_scoring_result("Date Recency", "Obs123", 0.85)
```

---

#### 5. `add_to_report`

**Syntax**:
```python
def add_to_report(self, scoring_name, total_scoring_applied, result_counts):
    pass
```

**Parameters**:
- `scoring_name` (str): The name of the scoring assessment.
- `total_scoring_applied` (int): The number of assessments applied for this scoring.
- `result_counts` (dict): Dictionary with counts of score categories (e.g., minimum, average, maximum).

**Description**:
The `add_to_report` function writes scoring summary information to the report file, including details such as the number of scores and the minimum, maximum, and average results.

**Example**:
```python
scoring_manager.add_to_report("Completeness Score", 100, {"Min": 0.1, "Avg": 0.5, "Max": 0.9})
```

---

#### 6. `extract_record_number`

**Syntax**:
```python
@staticmethod
def extract_record_number(record_uri):
    pass
```

**Parameters**:
- `record_uri` (str): The URI of the record to extract the number from.

**Description**:
The `extract_record_number` function extracts a unique record number from the given URI. This function is used for uniquely identifying records within the assessment.

**Example**:
```python
record_number = ScoringManager.extract_record_number("http://example.com/record/12345")
print(record_number)  # Output: 12345
```

---

### Example Workflow Using `ScoringManager`

Below is an example workflow demonstrating how to use the `ScoringManager` class to set up and apply scoring on assessment data.

#### Step 1: Initialize the `ScoringManager` Class

1. Import and initialize `ScoringManager` with required files:
    ```python
    from scoring_manager import ScoringManager
    scoring_manager = ScoringManager("scoring_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
    ```

#### Step 2: Create Scoring Matrix

1. Set up the scoring matrix based on definitions:
    ```python
    scoring_manager.create_scoring_matrix()
    ```

#### Step 3: Apply Scoring Methods

1. Apply scoring based on the created matrix:
    ```python
    scoring_manager.apply_scoring_methods()
    ```

#### Step 4: Generate Report Summary

1. Add scoring details to the report:
    ```python
    scoring_manager.add_to_report("Date Recency Score", 200, {"Min": 0.2, "Avg": 0.6, "Max": 1.0})
    ```

---

### Additional Notes

- **Scoring Definition Format**: Ensure the scoring definitions file is formatted correctly in Excel with necessary columns and headers for weights and criteria.
- **Output File**: The scored data is written to the specified output Turtle file in RDF format, allowing integration with other RDF-based systems.

This concludes the guide for `scoring_manager.py` in DQAF. For further assistance, refer to the full DQAF documentation or contact support.


## DQAF - `usecase_manager.py` Guide

This guide provides a comprehensive overview of the `usecase_manager.py` module in the Data Quality Assessment Framework (DQAF). The `usecase_manager.py` file is responsible for managing specific use case assessments, including creating and applying use case criteria to evaluate data quality.

---

### Overview of the `UseCaseManager` Class

The `UseCaseManager` class in `usecase_manager.py` manages use cases defined for data quality assessment. This class loads use case definitions, applies criteria based on user specifications, and generates structured results that contribute to the overall quality assessment.

#### Key Functions in `UseCaseManager`

Each function in `UseCaseManager` facilitates a unique aspect of use case management, from creating a use case matrix to assessing criteria and generating results. Below is a breakdown of each function, including its purpose, parameters, and usage examples.

#### 1. Initialization - `__init__`

**Syntax**:
```python
def __init__(self, use_case_definition_excel_file, assess_matrix_df, results_ttl, output_result_file, report_file=None):
    pass
```

**Parameters**:
- `use_case_definition_excel_file` (str): Path to the Excel file containing use case definitions.
- `assess_matrix_df` (pd.DataFrame): DataFrame holding assessment data for use cases.
- `results_ttl` (str): Path to the Turtle file with existing results to load.
- `output_result_file` (str): File path for saving the output results in Turtle format.
- `report_file` (file object, optional): File object for writing the use case assessment report.

**Description**:
The `__init__` method initializes the `UseCaseManager`, loading use case definitions and setting up matrices and files needed for output. This setup prepares the manager to perform assessments based on predefined use cases.

**Example**:
```python
use_case_manager = UseCaseManager("use_case_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
```

---

#### 2. `create_use_case_matrix`

**Syntax**:
```python
def create_use_case_matrix(self):
    pass
```

**Description**:
The `create_use_case_matrix` function loads use case definitions from the specified Excel file and organizes them into a matrix format. This matrix details the criteria for each use case, including specific conditions and thresholds.

**Example**:
```python
use_case_manager.create_use_case_matrix()
print("Use case matrix created successfully.")
```

---

#### 3. `assess_use_cases`

**Syntax**:
```python
def assess_use_cases(self):
    pass
```

**Description**:
The `assess_use_cases` function iterates through each use case in the matrix and applies defined conditions to the data. This function evaluates whether each record meets the specified criteria, and it compiles the results for reporting.

**Example**:
```python
use_case_manager.assess_use_cases()
print("Use cases assessed successfully.")
```

---

#### 4. `_add_use_case_assessment_result`

**Syntax**:
```python
def _add_use_case_assessment_result(self, use_case, observation_id, value, assessment_date=None):
    pass
```

**Parameters**:
- `use_case` (str): The name of the use case being assessed.
- `observation_id` (str or int): The unique identifier of the observation being assessed.
- `value` (bool): The result of the assessment (True if criteria are met, False otherwise).
- `assessment_date` (datetime, optional): The date of the assessment. Defaults to the current date.

**Description**:
The `_add_use_case_assessment_result` function adds the assessment result as a new RDF triple to the RDF graph. Each result stores whether an observation met the use case criteria, facilitating structured data quality tracking.

**Example**:
```python
use_case_manager._add_use_case_assessment_result("Location Completeness", "Obs123", True)
```

---

#### 5. `add_to_report`

**Syntax**:
```python
def add_to_report(self, assessment_name, total_assessments, result_counts):
    pass
```

**Parameters**:
- `assessment_name` (str): The name of the use case assessment.
- `total_assessments` (int): The number of records assessed for this use case.
- `result_counts` (dict): Dictionary containing counts of True and False assessments.

**Description**:
The `add_to_report` function writes a summary of the use case assessment results to the report file, including the total number of records assessed and the count of successful and unsuccessful assessments.

**Example**:
```python
use_case_manager.add_to_report("Date Completeness", 150, {"True": 120, "False": 30})
```

---

#### 6. `extract_record_number`

**Syntax**:
```python
@staticmethod
def extract_record_number(record_uri):
    pass
```

**Parameters**:
- `record_uri` (str): The URI of the record to extract the number from.

**Description**:
The `extract_record_number` function retrieves the unique record number from the specified URI, helping to identify individual records within the use case assessments.

**Example**:
```python
record_number = UseCaseManager.extract_record_number("http://example.com/record/12345")
print(record_number)  # Output: 12345
```

---

### Example Workflow Using `UseCaseManager`

Below is an example workflow demonstrating how to use the `UseCaseManager` class to set up and assess use cases for data quality.

#### Step 1: Initialize the `UseCaseManager` Class

1. Import and initialize `UseCaseManager` with necessary files:
    ```python
    from usecase_manager import UseCaseManager
    use_case_manager = UseCaseManager("use_case_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
    ```

#### Step 2: Create Use Case Matrix

1. Set up the use case matrix based on definitions:
    ```python
    use_case_manager.create_use_case_matrix()
    ```

#### Step 3: Assess Use Cases

1. Apply use case criteria to the assessment data:
    ```python
    use_case_manager.assess_use_cases()
    ```

#### Step 4: Add Assessment Summary to Report

1. Write the use case summary to the report file:
    ```python
    use_case_manager.add_to_report("Location Completeness", 200, {"True": 180, "False": 20})
    ```

---

### Additional Notes

- **Use Case Definition Format**: Ensure that the use case definitions file is correctly formatted in Excel with necessary columns and headers.
- **Output File**: The assessed data is saved to the specified output Turtle file, structured for compatibility with RDF-based applications.

This concludes the guide for `usecase_manager.py` in DQAF. For further assistance, refer to the full DQAF documentation or contact support.



## DQAF - Testing and Validation Guide

This guide provides an overview of the testing and validation process for the Data Quality Assessment Framework (DQAF). Testing and validation are essential to ensure that DQAF components work as expected, generating accurate and reliable assessments.

---

### 1. Preparing for Testing

To begin testing DQAF, ensure that all files, dependencies, and configuration settings are correctly set up. Review the following checklist:

- **Data Files**: Ensure all required input files (e.g., RDF, Excel for scoring and use case definitions) are available in the correct directory.
- **Configuration Files**: Confirm that configuration files (e.g., config.json) are set with correct paths and parameters.
- **Virtual Environment**: Activate the virtual environment if one is set up to isolate dependencies.

#### Example of Activating the Environment

1. Navigate to the project directory and activate the environment:
   - **On Windows**:
     ```bash
     dqaf_env\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source dqaf_env/bin/activate
     ```

2. Confirm that all required packages are installed. If any are missing, install them as follows:
   ```bash
   pip install numpy pandas rdflib openpyxl
   ```

---

### 2. Running Tests

Testing DQAF can be done in stages, focusing on individual modules (e.g., scoring, use cases, RDF processing) or the entire framework.

#### Running the Main Script

To conduct a full test, run the main script to ensure that all components function together:

```bash
python __main__.py
```

This test runs the entire assessment sequence, from loading data to generating the report.

#### Testing Individual Modules

Testing each module separately allows for focused troubleshooting.

1. **Vocabulary Manager**: Verify vocabulary loading and validation.
   ```python
   from vocab_manager import VocabManager
   vocab_manager = VocabManager()
   vocab_manager.load_vocab("path/to/vocab_file.csv")
   invalid_terms = vocab_manager.validate_vocab(["term1", "term2"])
   print(invalid_terms)
   ```

2. **RDF Query Processor**: Test RDF queries to confirm data extraction.
   ```python
   from query_processor import RDFQueryProcessor
   query_processor = RDFQueryProcessor("path/to/rdf_data.ttl")
   results = query_processor.execute_query("property_uri", "state_uri")
   query_processor.print_results(results)
   ```

3. **Report Analysis**: Check data analysis functionality and report generation.
   ```python
   from rdflib import Graph
   from report_analysis import ReportAnalysis
   rdf_graph = Graph().parse("rdf_data.ttl", format="turtle")
   report_analysis = ReportAnalysis(rdf_graph, report_file=open("report.txt", "w"))
   report_analysis.generate_report()
   ```

4. **Scoring Manager**: Test scoring calculations.
   ```python
   from scoring_manager import ScoringManager
   scoring_manager = ScoringManager("scoring_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
   scoring_manager.create_scoring_matrix()
   scoring_manager.apply_scoring_methods()
   ```

5. **Use Case Manager**: Validate use case assessments.
   ```python
   from usecase_manager import UseCaseManager
   use_case_manager = UseCaseManager("use_case_definitions.xlsx", assess_matrix_df, "results.ttl", "output.ttl")
   use_case_manager.create_use_case_matrix()
   use_case_manager.assess_use_cases()
   ```

---

### 3. Validating Outputs

After running tests, examine the output files to validate results. Key files to review include:

- **Report File**: Check the `.ttl` or `.txt` report for accuracy in the assessment summary.
- **Console Output**: Console messages during execution often provide feedback on successful operations or issues encountered.

#### Example Output Check

1. **Console Logs**:
   ```plaintext
   Starting Data Quality Assessment Framework (DQAF)...
   Vocabulary loaded successfully.
   RDF data processed successfully.
   Report generated at output/report.ttl.
   ```

2. **Report Sample**:
   ```plaintext
   @prefix dqaf: <https://example.com/def/dqaf/> .
   _:obs123 dqaf:hasDQAFResult "High Quality" .
   _:obs124 dqaf:hasDQAFResult "Low Quality" .
   ```

---

### 4. Troubleshooting Common Issues

#### Issue 1: Missing Dependencies

If you receive errors about missing libraries, ensure that the environment is activated and all required packages are installed:

```bash
pip install numpy pandas rdflib openpyxl
```

#### Issue 2: File Not Found Errors

If an input file is missing or misconfigured, verify the file paths in configuration files and command parameters.

#### Issue 3: Incorrect Output or Scores

If scores or results do not seem accurate, check the following:
- Confirm that the scoring definitions and use case files are correctly formatted.
- Review any thresholds or parameters in configuration files.

#### Issue 4: RDF Parsing Errors

If there are issues loading RDF data, ensure that the data file is valid and formatted correctly (e.g., Turtle format for `.ttl` files).

---

### 5. Automating Tests

For larger projects or repeated testing, consider automating tests using Python’s `unittest` module. This allows for structured testing of each function and can be expanded as new features are added.

#### Example Unit Test

```python
import unittest
from vocab_manager import VocabManager

class TestVocabManager(unittest.TestCase):
    def test_load_vocab(self):
        vocab_manager = VocabManager()
        vocab_manager.load_vocab("path/to/vocab_file.csv")
        self.assertIsNotNone(vocab_manager.validate_vocab(["valid_term"]))

if __name__ == "__main__":
    unittest.main()
```

---

### Additional Notes

- **Documentation**: Refer to the DQAF documentation for details on each module and parameter.
- **Log Files**: Consider adding logging to capture runtime information, which can help during troubleshooting and validation.

This concludes the testing and validation guide for DQAF. For further assistance, consult the development team or support resources.
---

