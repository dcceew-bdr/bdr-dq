from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# ===============================
# Define the namespace for terms
# ===============================
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
TIME = Namespace("http://www.w3.org/2006/time#")

def create_date_completeness_test_data():
    """
    This function creates RDF data to test the date completeness rule.

    It includes three test cases:
    - One observation with a complete date (→ non_empty)
    - One observation with no time or date at all (→ empty)
    - One observation with time but missing actual year (→ empty)
    """

    g = Graph()

    # ===============================
    # Observation 1: Has a complete date
    # ===============================
    g.add((TERN["obs_with_date"], RDF.type, TERN.Observation))
    g.add((TERN["obs_with_date"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2020", datatype=XSD.gYear)))

    # ===============================
    # Observation 2: No date or time at all
    # ===============================
    g.add((TERN["obs_no_date"], RDF.type, TERN.Observation))

    # ===============================
    # Observation 3: Has time, but missing actual date value
    # ===============================
    g.add((TERN["obs_missing_date"], RDF.type, TERN.Observation))
    g.add((TERN["obs_missing_date"], TIME.hasTime, TERN["time2"]))
    # No inXSDgYear for time2

    return g.serialize(format="turtle")

# Test run
if __name__ == "__main__":
    print(create_date_completeness_test_data())
