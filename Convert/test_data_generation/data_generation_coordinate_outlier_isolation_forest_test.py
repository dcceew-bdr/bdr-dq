from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

# RDF namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_isolation_forest_test_data():
    g = Graph()

    # 100 test points near Sydney (normal)
    for i in range(100):
        lon = round(151.2 + random.uniform(-0.05, 0.05), 6)
        lat = round(-33.9 + random.uniform(-0.05, 0.05), 6)
        add_test_observation(g, i, lon, lat)

    # 100 test points near Queensland (normal)
    for i in range(100, 200):
        lon = round(153.0 + random.uniform(-0.05, 0.05), 6)
        lat = round(-27.5 + random.uniform(-0.05, 0.05), 6)
        add_test_observation(g, i, lon, lat)

    # 10 test outlier points scattered
    for i in range(200, 210):
        lon = round(random.uniform(130.0, 160.0), 6)
        lat = round(random.uniform(-40.0, -10.0), 6)
        add_test_observation(g, i, lon, lat)

    return g.serialize(format="turtle")

def add_test_observation(g, idx, lon, lat):
    obs = EX[f"obs_{idx}"]
    sample = EX[f"sample_{idx}"]
    proc = EX[f"proc_{idx}"]
    geom = EX[f"geom_{idx}"]

    g.add((obs, RDF.type, TERN.Observation))
    g.add((obs, SOSA.hasFeatureOfInterest, sample))
    g.add((sample, RDF.type, TERN.Sample))
    g.add((sample, SOSA.isResultOf, proc))
    g.add((proc, GEO.hasGeometry, geom))
    g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

if __name__ == "__main__":
    ttl_data = create_coordinate_outlier_isolation_forest_test_data()
    with open("test_data_isolation_forest.ttl", "w") as f:
        f.write(ttl_data)
    print("Test RDF data saved to test_data_isolation_forest.ttl")
