from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")


def create_coordinate_unusual_pattern_test_data():
    """
    Generates RDF test data to assess unusual patterns in coordinate decimals.

    - "obs_usual_coords" → Normal decimal precision → should be labeled "usual"
    - "obs_repeating_digits" → Repeating digits like 145.111111 → should be "unusual"
    - "obs_pattern_repeats" → Pattern like 145.123123123 → should be "unusual"
    """

    g = Graph()

    # === Observation 1: Usual coordinate (should return "usual") ===
    g.add((TERN["obs_usual_coords"], RDF.type, TERN.Observation))
    g.add((TERN["obs_usual_coords"], SOSA.hasFeatureOfInterest, TERN["sample_usual"]))
    g.add((TERN["sample_usual"], RDF.type, TERN.Sample))
    g.add((TERN["sample_usual"], SOSA.isResultOf, TERN["procedure_usual"]))
    g.add((TERN["procedure_usual"], GEO.hasGeometry, TERN["geometry_usual"]))
    g.add((TERN["geometry_usual"], GEO.asWKT, Literal("POINT(145.6789 -37.9543)", datatype=XSD.string)))

    # === Observation 2: Repeating digit pattern (should return "unusual") ===
    g.add((TERN["obs_repeating_digits"], RDF.type, TERN.Observation))
    g.add((TERN["obs_repeating_digits"], SOSA.hasFeatureOfInterest, TERN["sample_repeat"]))
    g.add((TERN["sample_repeat"], RDF.type, TERN.Sample))
    g.add((TERN["sample_repeat"], SOSA.isResultOf, TERN["procedure_repeat"]))
    g.add((TERN["procedure_repeat"], GEO.hasGeometry, TERN["geometry_repeat"]))
    g.add((TERN["geometry_repeat"], GEO.asWKT, Literal("POINT(145.111111 -37.999)", datatype=XSD.string)))

    # === Observation 3: Repeating pattern like 123123 (should return "unusual") ===
    g.add((TERN["obs_pattern_repeats"], RDF.type, TERN.Observation))
    g.add((TERN["obs_pattern_repeats"], SOSA.hasFeatureOfInterest, TERN["sample_pattern"]))
    g.add((TERN["sample_pattern"], RDF.type, TERN.Sample))
    g.add((TERN["sample_pattern"], SOSA.isResultOf, TERN["procedure_pattern"]))
    g.add((TERN["procedure_pattern"], GEO.hasGeometry, TERN["geometry_pattern"]))
    g.add((TERN["geometry_pattern"], GEO.asWKT, Literal("POINT(145.123123123 -37.456456456)", datatype=XSD.string)))

    return g.serialize(format="turtle")


# Run this file directly to see the output
if __name__ == "__main__":
    turtle_data = create_coordinate_unusual_pattern_test_data()
    print(turtle_data)
