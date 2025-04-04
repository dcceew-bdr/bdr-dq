from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# ===============================
# Define the namespace for terms
# ===============================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
TIME = Namespace("http://www.w3.org/2006/time#")


def create_date_recency_test_data():
    """
    This function creates RDF data to test the date recency rule.

    It includes three test cases:
    - One observation with a recent date (after 2005) → expected: "recent_20_years"
    - One observation with an old date (before 2005) → expected: "outdated_20_years"
    - One observation with no date → should not be included in the results
    """

    # Create a new RDF graph to hold the test data
    g = Graph()

    # ============================================================
    # Observation 1: Recent observation (year = 2022)
    # This date is after 2005, so it should be labeled "recent_20_years"
    # ============================================================
    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    # ============================================================
    # Observation 2: Old observation (year = 1800)
    # This date is before 2005, so it should be labeled "outdated_20_years"
    # ============================================================
    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    # ============================================================
    # Observation 3: Missing date
    # This observation does not have a year, so it should be ignored
    # ============================================================
    g.add((TERN["observation3"], RDF.type, TERN.Observation))
    g.add((TERN["observation3"], TIME.hasTime, TERN["time3"]))
    # No inXSDgYear value for time3 → treated as missing

    # Return the graph content in Turtle (text) format
    return g.serialize(format="turtle")


# Run this file directly to print the test data to the terminal
if __name__ == "__main__":
    print(create_date_recency_test_data())
