from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# Define the namespace for observations.
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

def create_test_graph():
    """
    Creates an RDF graph with test_dq data for date recency checks.
    Returns the RDF graph serialized in Turtle format instead of saving to a file.
    """

    # Create an empty RDF graph to store test_dq data.
    g = Graph()

    # Add the first observation with a date in 2022 (recent case).
    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    # Add the second observation with a date in 1800 (outdated case).
    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    # Add the third observation without a date (to test_dq missing date scenarios).
    g.add((TERN["observation3"], RDF.type, TERN.Observation))

    # Return the RDF data serialized in Turtle format.
    return g.serialize(format="turtle")

# Run the function and print the generated test_dq data.
if __name__ == "__main__":
    turtle_data = create_test_graph()
    print(turtle_data)
