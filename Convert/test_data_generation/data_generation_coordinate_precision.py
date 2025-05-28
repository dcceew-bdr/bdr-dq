from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define vocabularies for RDF data
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_precision_test_data():
    """
    Make RDF test data to check coordinate precision level.

    It adds 3 test cases:
    - One with many decimal numbers → should be "High" precision
    - One with few decimal numbers → should be "Low"
    - One with normal decimal numbers → should be "Medium"
    """

    g = Graph()

    # === First test: high precision (more than 4 decimal places)
    g.add((EX["obs_high"], RDF.type, TERN.Observation))
    g.add((EX["obs_high"], SOSAN.hasFeatureOfInterest, EX["sample_high"]))
    g.add((EX["sample_high"], RDF.type, TERN.Sample))
    g.add((EX["sample_high"], SOSAN.isResultOf, EX["procedure_high"]))
    g.add((EX["procedure_high"], GEO.hasGeometry, EX["geometry_high"]))
    g.add((EX["geometry_high"], GEO.asWKT, Literal("POINT(150.123456 -34.987654)", datatype=XSD.string)))

    # === Second test: low precision (less than 2 decimal places)
    g.add((EX["obs_low"], RDF.type, TERN.Observation))
    g.add((EX["obs_low"], SOSAN.hasFeatureOfInterest, EX["sample_low"]))
    g.add((EX["sample_low"], RDF.type, TERN.Sample))
    g.add((EX["sample_low"], SOSAN.isResultOf, EX["procedure_low"]))
    g.add((EX["procedure_low"], GEO.hasGeometry, EX["geometry_low"]))
    g.add((EX["geometry_low"], GEO.asWKT, Literal("POINT(150.1 -34.9)", datatype=XSD.string)))

    # === Third test: medium precision (between 2 and 4 decimal places)
    g.add((EX["obs_medium"], RDF.type, TERN.Observation))
    g.add((EX["obs_medium"], SOSAN.hasFeatureOfInterest, EX["sample_medium"]))
    g.add((EX["sample_medium"], RDF.type, TERN.Sample))
    g.add((EX["sample_medium"], SOSAN.isResultOf, EX["procedure_medium"]))
    g.add((EX["procedure_medium"], GEO.hasGeometry, EX["geometry_medium"]))
    g.add((EX["geometry_medium"], GEO.asWKT, Literal("POINT(150.123 -34.45)", datatype=XSD.string)))

    return g.serialize(format="turtle")

# Run this file to test the function
if __name__ == "__main__":
    print(create_coordinate_precision_test_data())
