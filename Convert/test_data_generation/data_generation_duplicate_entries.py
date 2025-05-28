from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime

# Set up RDF namespaces
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
TIME = Namespace("http://www.w3.org/2006/time#")
EX = Namespace("http://example.com/test/")


def create_duplicate_test_data():
    """
    This function makes RDF data to test duplicate detection.
    A duplicate is found if scientific name + year + location are the same.

    Includes:
    - 2 same records (should be duplicates)
    - 1 different record (should be unique)
    """
    g = Graph()

    def add_obs(obs_id, name, year, wkt):
        # Make URIs for all parts
        obs = EX[obs_id]
        feature = EX[f"{obs_id}_feature"]
        proc = EX[f"{obs_id}_proc"]
        geom = EX[f"{obs_id}_geom"]
        time_inst = EX[f"{obs_id}_time"]

        # Add triples to RDF
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, feature))
        g.add((feature, RDF.type, TERN.Sample))
        g.add((feature, DWC.scientificName, Literal(name)))
        g.add((feature, SOSA.isResultOf, proc))
        g.add((proc, GEO.hasGeometry, geom))
        g.add((geom, GEO.asWKT, Literal(wkt, datatype=XSD.string)))
        g.add((obs, TIME.hasTime, time_inst))
        g.add((time_inst, TIME.inXSDgYear, Literal(str(year), datatype=XSD.gYear)))

    # Two same → should be flagged as duplicates
    add_obs("obs1", "Acacia dealbata", 2020, "POINT(151.2 -33.9)")
    add_obs("obs2", "Acacia dealbata", 2020, "POINT(151.2 -33.9)")

    # One different → should be unique
    add_obs("obs3", "Eucalyptus globulus", 2021, "POINT(151.3 -33.8)")

    return g.serialize(format="turtle")


# Run to see output in console
if __name__ == "__main__":
    print(create_duplicate_test_data()[:1000])
