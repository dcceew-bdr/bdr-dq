from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# Use namespaces to define vocabulary
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
TIME = Namespace("http://www.w3.org/2006/time#")

def create_date_completeness_test_data():
    """
    Make RDF test data to check if date is provided or not.

    We create 3 observations:
    - One has a full date (should return "non_empty")
    - One has no time or date (should return "empty")
    - One has time link but no actual date value (should return "empty")
    """

    g = Graph()

    # Observation 1: Has full date info → non_empty
    g.add((TERN["obs_with_date"], RDF.type, TERN.Observation))
    g.add((TERN["obs_with_date"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2020", datatype=XSD.gYear)))

    # Observation 2: No time or date at all → empty
    g.add((TERN["obs_no_date"], RDF.type, TERN.Observation))

    # Observation 3: Has time but no date value → empty
    g.add((TERN["obs_missing_date"], RDF.type, TERN.Observation))
    g.add((TERN["obs_missing_date"], TIME.hasTime, TERN["time2"]))
    # No inXSDgYear for time2

    return g.serialize(format="turtle")

# For quick test
if __name__ == "__main__":
    print(create_date_completeness_test_data())
