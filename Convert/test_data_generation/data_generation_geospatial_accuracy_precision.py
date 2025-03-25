from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define necessary namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


def create_geospatial_accuracy_precision_test_data():
    """
    Generates RDF data for geospatial accuracy precision checks:

    - obs_high_precision: accuracy <= 10,000 meters
    - obs_low_precision: accuracy > 10,000 meters
    - obs_missing_accuracy: no accuracy value provided
    """

    g = Graph()

    # === Observation 1: High precision (5000 meters) ===
    g.add((TERN["obs_high_precision"], RDF.type, TERN.Observation))
    g.add((TERN["obs_high_precision"], SOSA.hasFeatureOfInterest, TERN["sample_high"]))
    g.add((TERN["sample_high"], RDF.type, TERN.Sample))
    g.add((TERN["sample_high"], SOSA.isResultOf, TERN["procedure_high"]))
    g.add((TERN["procedure_high"], GEO.hasMetricSpatialAccuracy, Literal("5000", datatype=XSD.float)))

    # === Observation 2: Low precision (15000 meters) ===
    g.add((TERN["obs_low_precision"], RDF.type, TERN.Observation))
    g.add((TERN["obs_low_precision"], SOSA.hasFeatureOfInterest, TERN["sample_low"]))
    g.add((TERN["sample_low"], RDF.type, TERN.Sample))
    g.add((TERN["sample_low"], SOSA.isResultOf, TERN["procedure_low"]))
    g.add((TERN["procedure_low"], GEO.hasMetricSpatialAccuracy, Literal("15000", datatype=XSD.float)))

    # === Observation 3: Missing accuracy value (should be treated as low_precision) ===
    g.add((TERN["obs_missing_accuracy"], RDF.type, TERN.Observation))
    g.add((TERN["obs_missing_accuracy"], SOSA.hasFeatureOfInterest, TERN["sample_missing"]))
    g.add((TERN["sample_missing"], RDF.type, TERN.Sample))
    g.add((TERN["sample_missing"], SOSA.isResultOf, TERN["procedure_missing"]))
    # No accuracy triple added for procedure_missing

    return g.serialize(format="turtle")


# Run the function and print the generated RDF Turtle
if __name__ == "__main__":
    turtle_data = create_geospatial_accuracy_precision_test_data()
    print(turtle_data)
