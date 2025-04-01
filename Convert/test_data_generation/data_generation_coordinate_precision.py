from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# ===============================
# Define the namespaces used
# ===============================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_precision_test_data():
    """
    This function creates RDF test data to check coordinate precision.

    It includes:
    - One observation with high precision (more than 4 decimals)
    - One observation with low precision (less than 2 decimals)
    - One observation with medium precision (between 2 and 4 decimals)
    """

    g = Graph()

    # ======================================
    # Observation 1: High precision
    # WKT: POINT(150.123456 -34.987654) → "High"
    # ======================================
    g.add((EX["obs_high"], RDF.type, TERN.Observation))
    g.add((EX["obs_high"], SOSAN.hasFeatureOfInterest, EX["sample_high"]))
    g.add((EX["sample_high"], RDF.type, TERN.Sample))
    g.add((EX["sample_high"], SOSAN.isResultOf, EX["procedure_high"]))
    g.add((EX["procedure_high"], GEO.hasGeometry, EX["geometry_high"]))
    g.add((EX["geometry_high"], GEO.asWKT, Literal("POINT(150.123456 -34.987654)", datatype=XSD.string)))

    # ======================================
    # Observation 2: Low precision
    # WKT: POINT(150.1 -34.9) → "Low"
    # ======================================
    g.add((EX["obs_low"], RDF.type, TERN.Observation))
    g.add((EX["obs_low"], SOSAN.hasFeatureOfInterest, EX["sample_low"]))
    g.add((EX["sample_low"], RDF.type, TERN.Sample))
    g.add((EX["sample_low"], SOSAN.isResultOf, EX["procedure_low"]))
    g.add((EX["procedure_low"], GEO.hasGeometry, EX["geometry_low"]))
    g.add((EX["geometry_low"], GEO.asWKT, Literal("POINT(150.1 -34.9)", datatype=XSD.string)))

    # ======================================
    # Observation 3: Medium precision
    # WKT: POINT(150.123 -34.45) → "Medium"
    # ======================================
    g.add((EX["obs_medium"], RDF.type, TERN.Observation))
    g.add((EX["obs_medium"], SOSAN.hasFeatureOfInterest, EX["sample_medium"]))
    g.add((EX["sample_medium"], RDF.type, TERN.Sample))
    g.add((EX["sample_medium"], SOSAN.isResultOf, EX["procedure_medium"]))
    g.add((EX["procedure_medium"], GEO.hasGeometry, EX["geometry_medium"]))
    g.add((EX["geometry_medium"], GEO.asWKT, Literal("POINT(150.123 -34.45)", datatype=XSD.string)))

    return g.serialize(format="turtle")

# For manual testing
if __name__ == "__main__":
    print(create_coordinate_precision_test_data())
