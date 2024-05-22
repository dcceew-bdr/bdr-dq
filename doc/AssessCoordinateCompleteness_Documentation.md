
## Documentation for `assess_coordinate_completeness()` Method

### Overview

The `assess_coordinate_completeness()` method in the `RDFDataQualityAssessment` class checks if geographical coordinates (latitude and longitude) are provided for all relevant entries within an RDF graph. This method is crucial for ensuring that datasets intended for geographic analyses are complete and usable.

### Usage

This method should be invoked on an instance of the `RDFDataQualityAssessment` class that has been initialized with an RDF graph:

```python
# Assuming rdf_assessor is an instance of RDFDataQualityAssessment
rdf_assessor.assess_coordinate_completeness()
```

### How It Works

The method iterates over entries in the RDF graph that are expected to contain geographic information. It verifies whether each entry has both latitude and longitude data. Entries missing either coordinate are flagged as incomplete.

- **Non-empty:** Both latitude and longitude are present.
- **Empty:** Either latitude or longitude (or both) are missing.

### Example

```python
from rdflib import Graph

# Initialize the RDF graph
graph = Graph().parse("geo_data.ttl", format="ttl")

# Create an instance of the assessor
rdf_assessor = RDFDataQualityAssessment(graph)

# Perform the coordinate completeness assessment
rdf_assessor.assess_coordinate_completeness()

# Output completeness results
for result in rdf_assessor.result_matrix_df.itertuples():
    print(result)
```

### Conclusion

The `assess_coordinate_completeness()` method helps identify entries in RDF datasets that lack crucial geographic information, which is essential for completeness checks in spatial data analyses.
