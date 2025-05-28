from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

# Define common RDF vocabularies
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_zscore_test_data():
    """
    This function makes RDF test data for Z-score coordinate outlier check.

    It creates:
    - 100 points near Sydney (normal)
    - 100 points near Queensland (normal)
    - 10 random outlier points far from normal range
    - 3 manual points for testing
    """

    g = Graph()

    # Add 100 normal points close to Sydney
    for i in range(100):
        obs = EX[f"obs_{i}"]
        sample = EX[f"sample_{i}"]
        proc = EX[f"proc_{i}"]
        geom = EX[f"geom_{i}"]

        lon = round(151.2 + random.uniform(-0.05, 0.05), 6)
        lat = round(-33.9 + random.uniform(-0.05, 0.05), 6)

        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    # Add 100 normal points close to Queensland
    for i in range(100, 200):
        obs = EX[f"obs_{i}"]
        sample = EX[f"sample_{i}"]
        proc = EX[f"proc_{i}"]
        geom = EX[f"geom_{i}"]

        lon = round(153.0 + random.uniform(-0.05, 0.05), 6)
        lat = round(-27.5 + random.uniform(-0.05, 0.05), 6)

        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    # Add 10 outlier points in random faraway locations
    for i in range(200, 210):
        obs = EX[f"obs_{i}"]
        sample = EX[f"sample_{i}"]
        proc = EX[f"proc_{i}"]
        geom = EX[f"geom_{i}"]

        lon = round(random.uniform(140.0, 150.0), 6)
        lat = round(random.uniform(-40.0, -20.0), 6)

        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    # Add 3 specific test cases manually
    manual_points = [(151.25, -33.85), (150.0, -30.0), (152.9, -27.55)]
    for i, (lon, lat) in enumerate(manual_points, start=210):
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

    return g.serialize(format="turtle")

# Run and show some output
if __name__ == "__main__":
    print(create_coordinate_outlier_zscore_test_data()[:1000])
