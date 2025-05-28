from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# Define namespaces for terms used in RDF triples
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
TIME = Namespace("http://www.w3.org/2006/time#")

def create_date_recency_test_data():
    """
    This function makes test data to check if the year of each observation is recent or old.
    It gives:
    - One observation with recent year → should be "recent_20_years"
    - One with old year → should be "outdated_20_years"
    - One without date → ignored
    """

    g = Graph()

    # First observation: has year 2022 (after 2005)
    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    # Second observation: has year 1800 (before 2005)
    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    # Third observation: no year value → should be skipped
    g.add((TERN["observation3"], RDF.type, TERN.Observation))
    g.add((TERN["observation3"], TIME.hasTime, TERN["time3"]))
    # Missing year for time3

    return g.serialize(format="turtle")

# When run directly, show the data
if __name__ == "__main__":
    print(create_date_recency_test_data())
