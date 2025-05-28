from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

# define common namespaces (vocabularies)
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_isolation_forest_test_data():
    g = Graph()

    # create 200 normal points close to Sydney
    for i in range(200):
        lon = round(151.2 + random.uniform(-0.05, 0.05), 6)
        lat = round(-33.9 + random.uniform(-0.05, 0.05), 6)
        add_point(g, i, lon, lat)

    # create 200 normal points close to Queensland
    for i in range(200, 400):
        lon = round(153.0 + random.uniform(-0.05, 0.05), 6)
        lat = round(-27.5 + random.uniform(-0.05, 0.05), 6)
        add_point(g, i, lon, lat)

    # create 10 outlier points in random locations
    for i in range(400, 410):
        lon = round(random.uniform(130.0, 160.0), 6)
        lat = round(random.uniform(-40.0, -10.0), 6)
        add_point(g, i, lon, lat)

    # return RDF as turtle format
    return g.serialize(format="turtle")

def add_point(g, i, lon, lat):
    # make URIs for each RDF element
    obs = EX[f"obs_{i}"]
    sample = EX[f"sample_{i}"]
    proc = EX[f"proc_{i}"]
    geom = EX[f"geom_{i}"]

    # add triples for one observation point
    g.add((obs, RDF.type, TERN.Observation))
    g.add((obs, SOSA.hasFeatureOfInterest, sample))
    g.add((sample, RDF.type, TERN.Sample))
    g.add((sample, SOSA.isResultOf, proc))
    g.add((proc, GEO.hasGeometry, geom))
    g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

# run this part only if script is executed directly
if __name__ == "__main__":
    ttl_data = create_coordinate_outlier_isolation_forest_test_data()
    with open("test_data_isolation_forest.ttl", "w") as f:
        f.write(ttl_data)
    print("Test data saved to: test_data_isolation_forest.ttl")
