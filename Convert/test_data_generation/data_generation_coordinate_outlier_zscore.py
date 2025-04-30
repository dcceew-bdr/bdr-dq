from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_zscore_test_data():
    """
    Generate:
    - 190 normal points around (145, -36)
    - 10 outlier points slightly shifted
    """

    g = Graph()

    # === 190 Normal Observations ===
    for i in range(190):
        obs, sample, proc, geom = EX[f"obs_{i}"], EX[f"sample_{i}"], EX[f"proc_{i}"], EX[f"geom_{i}"]
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))

        lon = round(145 + random.uniform(-0.1, 0.1), 6)
        lat = round(-36 + random.uniform(-0.1, 0.1), 6)
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    # === 10 Outlier Observations ===
    for i in range(190, 200):
        obs, sample, proc, geom = EX[f"obs_{i}"], EX[f"sample_{i}"], EX[f"proc_{i}"], EX[f"geom_{i}"]
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))

        lon = round(145 + random.uniform(0.5, 1.0), 6)  # Farther
        lat = round(-36 + random.uniform(0.5, 1.0), 6)  # Farther
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    return g.serialize(format="turtle")

if __name__ == "__main__":
    print(create_coordinate_outlier_zscore_test_data())
