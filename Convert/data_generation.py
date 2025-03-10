from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

def create_test_graph():
    g = Graph()

    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    g.add((TERN["observation3"], RDF.type, TERN.Observation))

    g.serialize("test_data.ttl", format="turtle")
    print("Test data saved.")

if __name__ == "__main__":
    create_test_graph()
