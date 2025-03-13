from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# This script creates a small test dataset in RDF format.
# The dataset includes observations with dates to check if they are recent or outdated.

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# Define the namespace for observations.
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

def create_test_graph():
    # Create an empty RDF graph to store test data.
    g = Graph()

    # Add the first observation with a date in 2022 (recent case).
    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    # Add the second observation with a date in 1800 (outdated case).
    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    # Add the third observation without a date (to test missing date scenarios).
    g.add((TERN["observation3"], RDF.type, TERN.Observation))

    # Save the generated test data into a Turtle (.ttl) file.
    g.serialize("test_data.ttl", format="turtle")
    print("Test data saved.")

# Run the function to create and save the test dataset.
if __name__ == "__main__":
    create_test_graph()
