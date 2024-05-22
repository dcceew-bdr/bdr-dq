
## RDF Data Quality Assessment Documentation

This documentation explains the functionalities provided by the `RDFDataQualityAssessment` class, which is designed to perform various quality assessments on RDF data using GeoSPARQL and other semantic technologies.

### Overview

The `RDFDataQualityAssessment` class allows users to evaluate the quality of RDF data regarding geographical coordinates, dates, scientific names, and other properties. It relies heavily on libraries such as `rdflib`, `geopandas`, and `sklearn` to perform these assessments.

### Installation Requirements

Before you can use the `RDFDataQualityAssessment` class, ensure you have the following libraries installed:

- `rdflib`
- `numpy`
- `pandas`
- `geopandas`
- `shapely`
- `sklearn`

You can install these libraries using pip:

```bash
pip install rdflib numpy pandas geopandas shapely sklearn
```

### Usage

To use the `RDFDataQualityAssessment` class, you need to import it from its module, assuming it's in your project:

```python
from myproject.rdf_quality import RDFDataQualityAssessment
```

#### Initialization

Create an instance of the `RDFDataQualityAssessment` by specifying the RDF graph or a Path to a Turtle file:

```python
from rdflib import Graph
from pathlib import Path

# Using a Graph object
g = Graph().parse("data.ttl", format="ttl")
rdf_assessor = RDFDataQualityAssessment(g)

# Using a Path object
rdf_assessor = RDFDataQualityAssessment(Path("data.ttl"))
```

#### Performing Assessments

To perform all predefined data quality assessments:

```python
rdf_assessor.assessments()
```

### Methods

The class includes several methods to assess different aspects of data quality:

- `assess_coordinate_precision()`: Evaluates the precision of geographical coordinates.
- `assess_coordinate_completeness()`: Checks if geographical coordinates are provided.
- `assess_coordinate_unusual()`: Detects unusual patterns in coordinates.
- `assess_coordinate_in_australia_state()`: Verifies if coordinates fall within any Australian state boundaries.
- `assess_coordinate_outlier_irq()`: Identifies outliers using the Interquartile Range method.
- `assess_coordinate_outlier_zscore()`: Identifies outliers using the Z-score method.
- `assess_date_recency()`: Checks if dates are within the last 20 years.
- `assess_date_completeness()`: Checks if date fields are filled.
- `assess_date_outlier_kmeans()`: Identifies date outliers using the K-Means clustering method.
- `assess_date_format_validation()`: Validates the format of date strings.
- `assess_scientific_name_completeness()`: Checks if scientific names are provided.
- `assess_scientific_name_validation()`: Validates the correctness of scientific names.
- `assess_datum_completeness()`: Checks for the presence of datum information.
- `assess_datum_type()`: Evaluates the type of datum used.
- `assess_datum_validation()`: Validates the correctness of the datum.

### Example

Here is a detailed example of using `RDFDataQualityAssessment` to assess the quality of RDF data:

```python
from rdflib import Graph

# Initialize the RDF graph
graph = Graph().parse("example_data.ttl", format="ttl")

# Create an instance of the assessor
rdf_assessor = RDFDataQualityAssessment(graph)

# Perform all assessments
rdf_assessor.assessments()

# Output results
for result in rdf_assessor.result_matrix_df.itertuples():
    print(result)
```

### Conclusion

The `RDFDataQualityAssessment` class provides a comprehensive toolset for evaluating the quality of RDF data in terms of geographic and temporal accuracy, as well as the completeness and validation of the data contents. It's tailored for use in applications requiring high levels of data integrity, such as environmental data analysis and geospatial data management.
