from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

# =====================
# Define RDF namespaces
# =====================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_iqr_test_data():
    """
    This function create test RDF data for IQR-based coordinate outlier detection.

    It includes:
    - 100 normal points near Sydney
    - 100 normal points near Queensland
    - 10 outlier points far from both groups
    - 3 manual points for checking

    Output: RDF Turtle format as string
    """
    g = Graph()

    # ==== Add 100 points around Sydney area ====
    for i in range(100):
        lon = round(151.2 + random.uniform(-0.05, 0.05), 6)
        lat = round(-33.9 + random.uniform(-0.05, 0.05), 6)
        add_point(g, i, lon, lat)

    # ==== Add 100 points around Queensland area ====
    for i in range(100, 200):
        lon = round(153.0 + random.uniform(-0.05, 0.05), 6)
        lat = round(-27.5 + random.uniform(-0.05, 0.05), 6)
        add_point(g, i, lon, lat)

    # ==== Add 10 outlier points (far locations) ====
    for i in range(200, 210):
        lon = round(random.uniform(240.0, 150.0), 6)
        lat = round(random.uniform(-40.0, -20.0), 6)
        add_point(g, i, lon, lat)

    # ==== Add 3 special points manually ====
    manual_points = [(151.25, -33.85), (150.0, -30.0), (152.9, -27.55)]
    for i, (lon, lat) in enumerate(manual_points, start=210):
        add_point(g, i, lon, lat)

    return g.serialize(format="turtle")

def add_point(g, i, lon, lat):
    """
    Helper function to add RDF triples for one observation
    """
    obs = EX[f"obs_{i}"]
    sample = EX[f"sample_{i}"]
    proc = EX[f"proc_{i}"]
    geom = EX[f"geom_{i}"]

    g.add((obs, RDF.type, TERN.Observation))
    g.add((obs, SOSA.hasFeatureOfInterest, sample))
    g.add((sample, RDF.type, TERN.Sample))
    g.add((sample, SOSA.isResultOf, proc))
    g.add((proc, GEO.hasGeometry, geom))
    g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

# ===== Test run when script is run directly =====
if __name__ == "__main__":
    ttl_data = create_coordinate_outlier_iqr_test_data()
    print(ttl_data[:1000])  # print first 1000 characters only
