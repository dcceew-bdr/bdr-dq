from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# ================================
# Step 1: Define RDF namespaces
# ================================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_unusual_test_data():
    """
    This function creates test RDF data for assessing coordinate unusual patterns.

    The test includes:
    - One observation with decimal repeating digit (e.g., 45.111111) → "unusual"
    - One observation with repeating number pattern (e.g., 45.123123123) → "unusual"
    - One observation with no repeating pattern (e.g., 43.147893) → "usual"
    """

    g = Graph()

    # === Observation 1: Unusual - repeating digit pattern (e.g., 111111)
    g.add((EX["obs_unusual_digit"], RDF.type, TERN.Observation))
    g.add((EX["obs_unusual_digit"], SOSA.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSA.isResultOf, EX["proc1"]))
    g.add((EX["proc1"], GEO.hasGeometry, EX["geom1"]))
    g.add((EX["geom1"], GEO.asWKT, Literal("POINT(45.111111 -33.111111)", datatype=XSD.string)))

    # === Observation 2: Unusual - repeating number pattern (e.g., 123123123)
    g.add((EX["obs_unusual_pattern"], RDF.type, TERN.Observation))
    g.add((EX["obs_unusual_pattern"], SOSA.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSA.isResultOf, EX["proc2"]))
    g.add((EX["proc2"], GEO.hasGeometry, EX["geom2"]))
    g.add((EX["geom2"], GEO.asWKT, Literal("POINT(45.123123123 -34.145145145)", datatype=XSD.string)))

    # === Observation 3: Usual - normal decimal pattern
    g.add((EX["obs_usual"], RDF.type, TERN.Observation))
    g.add((EX["obs_usual"], SOSA.hasFeatureOfInterest, EX["sample3"]))
    g.add((EX["sample3"], RDF.type, TERN.Sample))
    g.add((EX["sample3"], SOSA.isResultOf, EX["proc3"]))
    g.add((EX["proc3"], GEO.hasGeometry, EX["geom3"]))
    g.add((EX["geom3"], GEO.asWKT, Literal("POINT(43.147893 -32.654321)", datatype=XSD.string)))

    return g.serialize(format="turtle")

# === For testing in console ===
if __name__ == "__main__":
    print(create_coordinate_unusual_test_data())
