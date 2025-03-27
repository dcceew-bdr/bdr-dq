from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")

def create_coordinate_precision_test_data():
    """
    Generates RDF test data for coordinate precision assessment.

    - "obs_low_precision": < 2 decimals → Should return "Low".
    - "obs_medium_precision": 3 or 4 decimals → Should return "Medium".
    - "obs_high_precision": > 4 decimals → Should return "High".
    """

    g = Graph()

    # === Observation with LOW precision (1 decimal) ===
    g.add((TERN["obs_low_precision"], RDF.type, TERN.Observation))
    g.add((TERN["obs_low_precision"], SOSA.hasFeatureOfInterest, TERN["sample_low"]))
    g.add((TERN["sample_low"], RDF.type, TERN.Sample))
    g.add((TERN["sample_low"], SOSA.isResultOf, TERN["procedure_low"]))
    g.add((TERN["procedure_low"], GEO.hasGeometry, TERN["geometry_low"]))
    g.add((TERN["geometry_low"], GEO.asWKT, Literal("POINT(150.6 -34.3)", datatype=XSD.string)))  # 1 decimal

    # === Observation with MEDIUM precision (3 decimals) ===
    g.add((TERN["obs_medium_precision"], RDF.type, TERN.Observation))
    g.add((TERN["obs_medium_precision"], SOSA.hasFeatureOfInterest, TERN["sample_medium"]))
    g.add((TERN["sample_medium"], RDF.type, TERN.Sample))
    g.add((TERN["sample_medium"], SOSA.isResultOf, TERN["procedure_medium"]))
    g.add((TERN["procedure_medium"], GEO.hasGeometry, TERN["geometry_medium"]))
    g.add((TERN["geometry_medium"], GEO.asWKT, Literal("POINT(150.643 -34.397)", datatype=XSD.string)))  # 3 decimals

    # === Observation with HIGH precision (6 decimals) ===
    g.add((TERN["obs_high_precision"], RDF.type, TERN.Observation))
    g.add((TERN["obs_high_precision"], SOSA.hasFeatureOfInterest, TERN["sample_high"]))
    g.add((TERN["sample_high"], RDF.type, TERN.Sample))
    g.add((TERN["sample_high"], SOSA.isResultOf, TERN["procedure_high"]))
    g.add((TERN["procedure_high"], GEO.hasGeometry, TERN["geometry_high"]))
    g.add((TERN["geometry_high"], GEO.asWKT, Literal("POINT(150.644123 -34.397456)", datatype=XSD.string)))  # 6 decimals

    return g.serialize(format="turtle")

# Run the function to test output
if __name__ == "__main__":
    print(create_coordinate_precision_test_data())