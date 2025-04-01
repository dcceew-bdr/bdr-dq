from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF

# ===============================
# Define the namespace for terms
# ===============================
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_completeness_test_data():
    """
    This function creates RDF data to test the coordinate completeness rule.

    It includes:
    - One observation with complete coordinates (non_empty)
    - One observation without geometry (empty)
    - One observation with a sample and procedure, but missing the WKT value (empty)
    """

    g = Graph()

    # ====================================
    # Observation 1: Has complete geometry
    # → Should be classified as "non_empty"
    # ====================================
    g.add((EX["obs_with_coords"], RDF.type, TERN.Observation))
    g.add((EX["obs_with_coords"], SOSAN.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSAN.isResultOf, EX["procedure1"]))
    g.add((EX["procedure1"], GEO.hasGeometry, EX["geometry1"]))
    g.add((EX["geometry1"], GEO.asWKT, Literal("POINT(150.644 -34.397)", datatype=GEO.wktLiteral)))

    # ====================================
    # Observation 2: No geometry at all
    # → Should be classified as "empty"
    # ====================================
    g.add((EX["obs_no_coords"], RDF.type, TERN.Observation))
    g.add((EX["obs_no_coords"], SOSAN.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSAN.isResultOf, EX["procedure2"]))
    # No geometry at all for procedure2

    # ====================================
    # Observation 3: Has geometry node but no WKT
    # → Should be classified as "empty"
    # ====================================
    g.add((EX["obs_missing_wkt"], RDF.type, TERN.Observation))
    g.add((EX["obs_missing_wkt"], SOSAN.hasFeatureOfInterest, EX["sample3"]))
    g.add((EX["sample3"], RDF.type, TERN.Sample))
    g.add((EX["sample3"], SOSAN.isResultOf, EX["procedure3"]))
    g.add((EX["procedure3"], GEO.hasGeometry, EX["geometry3"]))
    # geometry3 has no WKT triple

    return g.serialize(format="turtle")

# For manual test
if __name__ == "__main__":
    print(create_coordinate_completeness_test_data())
