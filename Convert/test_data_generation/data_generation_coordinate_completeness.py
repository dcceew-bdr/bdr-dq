from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define namespaces for observations, geographic data, and samples
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")  # TERN namespace for observations
SOSA = Namespace("http://www.w3.org/ns/sosa/")  # SOSA namespace for feature relationships
GEO = Namespace("http://www.opengis.net/ont/geosparql#")  # Geospatial ontology

def create_coordinate_completeness_test_data():
    """
    Generates RDF test_dq data for coordinate completeness checks.

    - "obs_with_coordinates" → Has valid coordinates (WKT format) → Should return "non_empty".
    - "obs_missing_coordinates" → Missing WKT geometry → Should return "empty".
    """

    # Create an RDF graph (a structure to hold RDF data)
    g = Graph()

    # === Observation 1: Has valid coordinates (should be "non_empty") ===
    g.add((TERN["obs_with_coordinates"], RDF.type, TERN.Observation))  # Define an observation
    g.add((TERN["obs_with_coordinates"], SOSA.hasFeatureOfInterest, TERN["sample1"]))  # Link to a sample
    g.add((TERN["sample1"], RDF.type, TERN.Sample))  # Define the sample
    g.add((TERN["sample1"], SOSA.isResultOf, TERN["procedure1"]))  # Link sample to a procedure
    g.add((TERN["procedure1"], GEO.hasGeometry, TERN["geometry1"]))  # Link procedure to a geometry
    g.add((TERN["geometry1"], GEO.asWKT, Literal("POINT(150.644 -34.397)", datatype=XSD.string)))  # Has valid coordinates

    # === Observation 2: Missing coordinates (should be "empty") ===
    g.add((TERN["obs_missing_coordinates"], RDF.type, TERN.Observation))  # Define another observation
    g.add((TERN["obs_missing_coordinates"], SOSA.hasFeatureOfInterest, TERN["sample2"]))  # Link to another sample
    g.add((TERN["sample2"], RDF.type, TERN.Sample))  # Define this sample
    g.add((TERN["sample2"], SOSA.isResultOf, TERN["procedure2"]))  # Link it to a procedure
    g.add((TERN["procedure2"], GEO.hasGeometry, TERN["geometry2"]))  # Link to geometry
    # No WKT property added for geometry2 (should return "empty" in the test_dq)

    # Return the RDF data serialized in Turtle format instead of writing to a file
    return g.serialize(format="turtle")

# Run the function and print the generated test_dq data.
if __name__ == "__main__":
    turtle_data = create_coordinate_completeness_test_data()
    print(turtle_data)
