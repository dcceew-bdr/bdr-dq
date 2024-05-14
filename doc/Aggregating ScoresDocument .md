# Understanding Data Quality Assessment Scoring in Python

## Introduction

This document aims to explain a Python code file that helps in assessing the quality of data through scoring. This code is designed to manage scoring definitions, apply scoring methods to actual data, and generate reports based on the assessment results. 

## Overview

### 1. Importing Libraries

The code begins by importing several Python libraries:
- `datetime`: For handling dates and times.
- `numpy`: For numerical computations.
- `pandas`: For data manipulation and analysis.
- `rdflib`: For working with RDF (Resource Description Framework) graphs.
- Custom modules: These include `defined_namespaces` and `vocab_manager`.

### 2. Class Definition: ScoringManager

#### Initialization
- The `ScoringManager` class is initialized with various parameters like the path to the scoring definition Excel file, assessment data, output result file, and optionally a report file.
- It loads the scoring definition Excel file into a DataFrame.

#### Method: `create_scoring_matrix()`
- Reads the scoring definition Excel file and creates a scoring matrix.
- This matrix defines the scoring rules for different aspects of data quality.

#### Method: `apply_scoring_methods()`
- Applies the scoring methods defined in the scoring matrix to the assessment data.
- Calculates scores based on defined conditions and updates the result matrix.
- Adds scoring results to an RDF graph and saves it to a Turtle file.
- If provided, adds scoring assessment details to a report file.

### 3. Utility Functions

#### `flatten_dictionary()`
- Converts a nested dictionary into a single-level dictionary.
- Useful for simplifying complex structures for processing.

#### `dictionary_to_vector_and_keys()`
- Converts a dictionary into a numerical vector and retrieves the keys.
- This is handy for mathematical operations on dictionary values.

#### `calculate_subgroup_max_score()` and `calculate_subgroup_min_score()`
- Calculate maximum and minimum scores for subgroups within a dictionary.
- Useful for aggregating scores based on specific criteria.

## Example Usage

Let's say you have a dataset containing various attributes like 'accuracy', 'completeness', and 'consistency'. You want to assess the data quality based on these attributes.

1. **Define Scoring Rules:**
   - Create an Excel file containing scoring rules for each attribute. For example:
     ```
     | Data quality assertion | accuracy | completeness | consistency |
     |------------------------|----------|--------------|-------------|
     | Weight                 | 3        | 2            | 1           |
     ```

2. **Instantiate ScoringManager:**
   ```python
   manager = ScoringManager(scoring_definition_excel_file='scoring_rules.xlsx',
                            assess_matrix_df=data_df,
                            results_ttl='results.ttl',
                            output_result_file='result.ttl',
                            report_file='report.md')
   ```

3. **Apply Scoring Methods:**
   ```python
   manager.apply_scoring_methods()
   ```

4. **Review Results:**
   - Check the generated `result.ttl` file for detailed scoring results.
   - Review the `report.md` file for a summary of assessment outcomes.

## Conclusion

This Python code provides a robust framework for assessing data quality through scoring methods. By defining scoring rules and applying them to actual data, users can gain insights into the quality of their datasets. The code offers flexibility and extensibility for handling various data quality assessment scenarios.

---


# Data Quality Assessment Results

## Scoring Definition

| Data quality assertion | accuracy | completeness | consistency |
|------------------------|----------|--------------|-------------|
| Weight                 | 3        | 2            | 1           |

## Example Data

| Observation ID | accuracy | completeness | consistency |
|----------------|----------|--------------|-------------|
| 1              | 0.9      | 0.8          | 0.7         |
| 2              | 0.6      | 0.9          | 0.5         |
| 3              | 0.8      | 0.7          | 0.6         |

## Example Scoring

### Observation 1:
- Accuracy Score: 2.7
- Completeness Score: 1.6
- Consistency Score: 0.7
- **Total Score: 5.0**

### Observation 2:
- Accuracy Score: 1.8
- Completeness Score: 1.8
- Consistency Score: 0.5
- **Total Score: 4.1**

### Observation 3:
- Accuracy Score: 2.4
- Completeness Score: 1.4
- Consistency Score: 0.6
- **Total Score: 4.4**

## Results

Based on the scoring, here are the total scores for each observation:

- **Observation 1:** Total Score = 5.0
- **Observation 2:** Total Score = 4.1
- **Observation 3:** Total Score = 4.4

These scores indicate the overall quality of each observation based on the defined data quality assertions. Higher scores indicate better data quality.
