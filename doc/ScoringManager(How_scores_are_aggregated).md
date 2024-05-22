
# ScoringManager (How scores are aggregated)

## Introduction

This document aims to explain a Python code file that helps in assessing the overall quality of data through numeric scoring of records (fitness-for-purpose FFP, assessment), using weights determined by the data curator for a particular purpose (i.e. a particular FFP profile).

This code is designed to manage scoring definitions, apply scoring methods to actual data, and generate reports based on the assessment results.

There is also a way to assess the FFP of data using categorical scores, see (link to documentation when ready) for more information.

## What is Scoring?

Scoring refers to the process of evaluating data records to determine their suitability for specific purposes. This is done by assessing various dimensions of data quality, such as accuracy, completeness, and consistency, and aggregating these scores to provide an overall assessment.

## Relevant Python File

The scoring functionality is primarily implemented in the `scoring_manager.py` file.

## Input Data

The input data for the scoring process should be provided in an Excel file. The relative path for this file is in score folder.

## Output Data

The scoring results are stored in various output files, such as `result.ttl` and `report.md`. Relative paths should be used throughout the documentation to ensure consistency. Below is an example snippet of what the scoring outputs might look like:

```markdown
# Example Scoring Output
- `result.ttl`: Contains the aggregated scores in a turtle format.
- `report.md`: Provides a detailed report of the scoring process and results.
```

## Example of Scoring

For the baseline SDM use case, the scoring includes evaluating `coordinate_precision` with levels such as Low, Medium, and High. This specific example demonstrates how the scoring mechanism assesses the fitness for purpose for data records.

### Example:
```python
# Scoring dimensions
accuracy = 0.9
completeness = 0.85
consistency = 0.95

# Fitness for purpose (FFP) example
coordinate_precision = "High"
```

## Directory Structure

Ensure that all files are placed in their appropriate directories with correct relative paths. This includes the input Excel file (assertions_score_weighting_definition.xlsx) and the output files like result.ttl and report.md.

## Conclusion

This guide has provided an overview of the scoring process and how it is implemented in the `scoring_manager.py` file. By following this guide, users can effectively assess the fitness for purpose of their data records for predefined purposes.

