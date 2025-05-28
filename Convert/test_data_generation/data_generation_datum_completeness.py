from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define common RDF namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")


def create_datum_completeness_test_data():
    """
    Make RDF test data to check if datum is missing or not.

    We create two observations:
    - One has datum → expected result: "not_empty"
    - One has no datum → expected result: "empty"
    """

    g = Graph()

    # First observation: has datum value (should be not_empty)
    g.add((EX["obs_with_datum"], RDF.type, TERN.Observation))
    g.add((EX["obs_with_datum"], SOSA.hasFeatureOfInterest, EX["sample1"]))
    g.add((EX["sample1"], RDF.type, TERN.Sample))
    g.add((EX["sample1"], SOSA.isResultOf, EX["proc1"]))
    g.add((EX["proc1"], GEO.hasGeometryDatum, Literal("EPSG:4326", datatype=XSD.string)))

    # Second observation: no datum value (should be empty)
    g.add((EX["obs_no_datum"], RDF.type, TERN.Observation))
    g.add((EX["obs_no_datum"], SOSA.hasFeatureOfInterest, EX["sample2"]))
    g.add((EX["sample2"], RDF.type, TERN.Sample))
    g.add((EX["sample2"], SOSA.isResultOf, EX["proc2"]))
    # No geo:hasGeometryDatum for proc2 → so it's missing

    return g.serialize(format="turtle")


# Print the data if this file runs directly
if __name__ == "__main__":
    print(create_datum_completeness_test_data())
