from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# =====================================
# Step 1: Define the RDF namespaces
# =====================================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_datum_completeness_test_data():
    """
    This function creates RDF test data for checking datum completeness.

    It includes:
    - One observation with datum → "not_empty"
    - One observation without datum → "empty"
    """

    g = Graph()

    # === Observation 1: With datum (should return "not_empty")
    g.add((EX["obs_with_datum"], RDF.type, TERN.Observation))
    g.add((EX["obs_with_datum"], SOSA.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSA.isResultOf, EX["proc1"]))
    g.add((EX["proc1"], GEO.hasGeometryDatum, Literal("EPSG:4326", datatype=XSD.string)))

    # === Observation 2: Without datum (should return "empty")
    g.add((EX["obs_no_datum"], RDF.type, TERN.Observation))
    g.add((EX["obs_no_datum"], SOSA.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSA.isResultOf, EX["proc2"]))
    # No geo:hasGeometryDatum triple here!

    return g.serialize(format="turtle")

# For testing the RDF generation manually
if __name__ == "__main__":
    print(create_datum_completeness_test_data())
