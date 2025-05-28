from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# ===============================
# Step 1: Define all used namespaces
# ===============================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_geospatial_accuracy_precision_test_data():
    """
    This function creates RDF test data to test how precise the coordinate is.

    It includes 3 types of cases:
    - One with low uncertainty (5.5 meters) → expected as 'high_precision'
    - One with large uncertainty (20000 meters) → expected as 'low_precision'
    - One with no uncertainty value → should also be 'low_precision'
    """

    g = Graph()

    # === Observation with high precision (uncertainty is small)
    g.add((EX["obs_high"], RDF.type, TERN.Observation))
    g.add((EX["obs_high"], SOSA.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSA.isResultOf, EX["proc1"]))
    g.add((EX["proc1"], GEO.hasMetricSpatialAccuracy, Literal("5.5", datatype=XSD.float)))

    # === Observation with low precision (uncertainty is big)
    g.add((EX["obs_low"], RDF.type, TERN.Observation))
    g.add((EX["obs_low"], SOSA.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSA.isResultOf, EX["proc2"]))
    g.add((EX["proc2"], GEO.hasMetricSpatialAccuracy, Literal("20000", datatype=XSD.float)))

    # === Observation with no uncertainty → we treat it as low precision
    g.add((EX["obs_missing"], RDF.type, TERN.Observation))
    g.add((EX["obs_missing"], SOSA.hasFeatureOfInterest, EX["sample3"]))
    g.add((EX["sample3"], RDF.type, TERN.Sample))
    g.add((EX["sample3"], SOSA.isResultOf, EX["proc3"]))
    # No spatial accuracy value is given here

    return g.serialize(format="turtle")

# Manual test: print result if run directly
if __name__ == "__main__":
    print(create_geospatial_accuracy_precision_test_data())
