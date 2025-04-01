from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# ===============================
# Step 1: Define common namespaces
# ===============================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_geospatial_accuracy_precision_test_data():
    """
    This function creates RDF test data to check geospatial accuracy precision.

    We test 3 cases:
    - Observation with uncertainty = 5.5 → should be 'high_precision'
    - Observation with uncertainty = 20000 → should be 'low_precision'
    - Observation with no uncertainty → should also be 'low_precision'
    """

    g = Graph()

    # === Case 1: High precision (uncertainty = 5.5)
    g.add((EX["obs_high"], RDF.type, TERN.Observation))
    g.add((EX["obs_high"], SOSA.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSA.isResultOf, EX["proc1"]))
    g.add((EX["proc1"], GEO.hasMetricSpatialAccuracy, Literal("5.5", datatype=XSD.float)))

    # === Case 2: Low precision (uncertainty = 20000)
    g.add((EX["obs_low"], RDF.type, TERN.Observation))
    g.add((EX["obs_low"], SOSA.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSA.isResultOf, EX["proc2"]))
    g.add((EX["proc2"], GEO.hasMetricSpatialAccuracy, Literal("20000", datatype=XSD.float)))

    # === Case 3: Missing uncertainty → should default to 'low_precision'
    g.add((EX["obs_missing"], RDF.type, TERN.Observation))
    g.add((EX["obs_missing"], SOSA.hasFeatureOfInterest, EX["sample3"]))
    g.add((EX["sample3"], RDF.type, TERN.Sample))
    g.add((EX["sample3"], SOSA.isResultOf, EX["proc3"]))
    # No accuracy triple added for this case

    return g.serialize(format="turtle")

# === For manual testing ===
if __name__ == "__main__":
    print(create_geospatial_accuracy_precision_test_data())
