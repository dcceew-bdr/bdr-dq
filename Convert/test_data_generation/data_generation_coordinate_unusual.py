from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Use standard RDF namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_coordinate_unusual_test_data():
    """
    Create RDF test data for coordinate unusualness check.
    This makes:
    - Two normal coordinates (around Sydney)
    - One strange/unusual coordinate (very far from normal)
    """

    g = Graph()

    # Helper function to add one observation with coordinates
    def add_point(obs_id, lon, lat):
        obs = EX[obs_id]
        sample = EX[f"{obs_id}_sample"]
        proc = EX[f"{obs_id}_proc"]
        geom = EX[f"{obs_id}_geom"]

        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))
        g.add((geom, GEO.asWKT, Literal(f"POINT({lon} {lat})", datatype=XSD.string)))

    # Add two typical coordinates (should be usual)
    add_point("obs_typical1", 151.2, -33.9)
    add_point("obs_typical2", 151.3, -33.8)

    # Add one unusual coordinate (far outside normal range)
    add_point("obs_unusual", 10.0, 10.0)

    return g.serialize(format="turtle")

# Print some of the RDF when running directly
if __name__ == "__main__":
    print(create_coordinate_unusual_test_data()[:1000])
