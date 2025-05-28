from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

# Define RDF namespaces
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_completeness_test_data():
    """
    Make test RDF data to check coordinate completeness.

    It creates 3 observations:
    1. With full geometry → should be 'non_empty'
    2. Without any geometry → should be 'empty'
    3. Has geometry node but no WKT → should be 'empty'
    """
    g = Graph()

    # Observation 1: With full coordinate (WKT exists)
    g.add((EX["obs_with_coords"], RDF.type, TERN.Observation))
    g.add((EX["obs_with_coords"], SOSAN.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSAN.isResultOf, EX["procedure1"]))
    g.add((EX["procedure1"], GEO.hasGeometry, EX["geometry1"]))
    g.add((EX["geometry1"], GEO.asWKT, Literal("POINT(150.644 -34.397)", datatype=GEO.wktLiteral)))

    # Observation 2: No geometry at all
    g.add((EX["obs_no_coords"], RDF.type, TERN.Observation))
    g.add((EX["obs_no_coords"], SOSAN.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSAN.isResultOf, EX["procedure2"]))
    # geometry is missing

    # Observation 3: Geometry node exists but WKT missing
    g.add((EX["obs_missing_wkt"], RDF.type, TERN.Observation))
    g.add((EX["obs_missing_wkt"], SOSAN.hasFeatureOfInterest, EX["sample3"]))
    g.add((EX["sample3"], RDF.type, TERN.Sample))
    g.add((EX["sample3"], SOSAN.isResultOf, EX["procedure3"]))
    g.add((EX["procedure3"], GEO.hasGeometry, EX["geometry3"]))
    # geometry3 exists, but has no WKT

    return g.serialize(format="turtle")

# Run manually to see RDF output
if __name__ == "__main__":
    print(create_coordinate_completeness_test_data())
