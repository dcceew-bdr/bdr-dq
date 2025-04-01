from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
import random

# Namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_outlier_iqr_test_data():
    """
    Generate:
    - 190 normal points
    - 10 outlier points
    - 5 labeled test cases (manually editable)
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

        lon = round(random.uniform(140.0, 150.0), 6)
        lat = round(random.uniform(-39.0, -32.0), 6)
        tag = "normal_coordinate"
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))
        print(f"{i+1:03d}. [{tag.upper()}] POINT({lon} {lat})")

    # === 10 Outliers ===
    for i in range(190, 200):
        obs, sample, proc, geom = EX[f"obs_{i}"], EX[f"sample_{i}"], EX[f"proc_{i}"], EX[f"geom_{i}"]
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))

        lon = round(random.uniform(160.0, 170.0), 6)
        lat = round(random.uniform(-50.0, -45.0), 6)
        tag = "outlier_coordinate"
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))
        print(f"{i+1:03d}. [{tag.upper()}] POINT({lon} {lat})")

    # === 5 Editable Manual Test Cases ===
    manual_cases = [
        ("obs_manual_1", 205.123456, -34.654321, "normal_coordinate"),   # Editable case
        ("obs_manual_2", 148.987654, -55.876543, "normal_coordinate"),   # Editable case
        ("obs_manual_3", 123.321789, -55.123456, "outlier_coordinate"),  # Editable case
        ("obs_manual_4", 169.654321, -49.765432, "outlier_coordinate"),  # Editable case
        ("obs_manual_5", 142.555555, -35.555555, "normal_coordinate")    # Editable case
    ]

    for i, (obs_id, lon, lat, tag) in enumerate(manual_cases, start=201):
        obs, sample, proc, geom = EX[obs_id], EX[f"sample_manual_{i}"], EX[f"proc_manual_{i}"], EX[f"geom_manual_{i}"]
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))

        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))
        print(f"{i:03d}. [MANUAL - {tag.upper()}] POINT({lon} {lat})")

    return g.serialize(format="turtle")

# Manual run
if __name__ == "__main__":
    create_coordinate_outlier_iqr_test_data()
