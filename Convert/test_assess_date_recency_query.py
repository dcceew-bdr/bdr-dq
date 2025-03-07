import pytest
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")


def create_test_graph():
    g = Graph()

    g.add((TERN["observation1"], RDF.type, TERN.Observation))
    g.add((TERN["observation1"], SOSA.hasFeatureOfInterest, TERN["sample1"]))
    g.add((TERN["sample1"], RDF.type, TERN.Sample))
    g.add((TERN["sample1"], SOSA.isResultOf, TERN["procedure1"]))
    g.add((TERN["procedure1"], TIME.hasTime, TERN["time1"]))
    g.add((TERN["time1"], TIME.inXSDgYear, Literal("2022", datatype=XSD.gYear)))

    g.add((TERN["observation2"], RDF.type, TERN.Observation))
    g.add((TERN["observation2"], SOSA.hasFeatureOfInterest, TERN["sample2"]))
    g.add((TERN["sample2"], RDF.type, TERN.Sample))
    g.add((TERN["sample2"], SOSA.isResultOf, TERN["procedure2"]))
    g.add((TERN["procedure2"], TIME.hasTime, TERN["time2"]))
    g.add((TERN["time2"], TIME.inXSDgYear, Literal("1800", datatype=XSD.gYear)))

    g.add((TERN["observation3"], RDF.type, TERN.Observation))
    g.add((TERN["observation3"], SOSA.hasFeatureOfInterest, TERN["sample3"]))
    g.add((TERN["sample3"], RDF.type, TERN.Sample))
    g.add((TERN["sample3"], SOSA.isResultOf, TERN["procedure3"]))
    g.add((TERN["procedure3"], TIME.hasTime, TERN["time3"]))

    return g


@pytest.fixture
def test_graph():
    return create_test_graph()


@pytest.fixture
def query():
    return """
    PREFIX tern: <https://w3id.org/tern/ontologies/tern/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX time: <http://www.w3.org/2006/time#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?observation ?date
    WHERE {
      ?observation a tern:Observation .
      ?observation sosa:hasFeatureOfInterest ?sample .
      ?sample a tern:Sample .
      ?sample sosa:isResultOf ?procedure .
      ?procedure time:hasTime ?ot .
      ?ot time:inXSDgYear ?date .
    }
    """


def test_date_recency_check(test_graph, query):
    results = test_graph.query(query)
    extracted_results = {str(row[0]): int(row[1]) for row in results}

    assert "https://w3id.org/tern/ontologies/tern/observation1" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation1"] >= 2000

    assert "https://w3id.org/tern/ontologies/tern/observation2" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation2"] < 1900

    assert "https://w3id.org/tern/ontologies/tern/observation3" not in extracted_results
