from datetime import datetime
from pathlib import Path

import pytest
from pyoxigraph import Store, RdfFormat, QueryResultsFormat
from rdflib import BNode, SOSA, URIRef, SDO, Literal, XSD, Graph, IdentifiedNode

from dq import DQAF
from dq.vocab_manager import VocabManager


QUERY_DIR = Path(__file__).parent / "queries"


def pytest_addoption(parser):
    parser.addoption(
        "--datafile",
        action="store",
        default=Path(__file__).parent.parent / "dq/input/combined_graph.ttl",
        help="Path to the turtle file to be validated against the DQF."
    )

@pytest.fixture(scope="session")
def store(request):
    datafile = request.config.getoption("datafile")
    store = Store()

    file_bytes = Path(datafile).read_bytes()
    store.load(file_bytes, RdfFormat.TURTLE)

    yield store

@pytest.fixture(scope="session")
def vocab_manager():
    return VocabManager()

@pytest.fixture(scope="session")
def get_observation_geometries(store):
    #TODO this query will need updating for the correct graph path to Geomtries. It is currently using a direct path in
    # order to test the functionality.
    """Observation geometries are reused in 14 different DQF assessments"""
    query = (QUERY_DIR/"fixture_get_obs_geoms.rq").read_text()
    return  store.query(query).serialize(format=QueryResultsFormat.CSV).decode()


@pytest.fixture(scope="session")
def result_graph():
    g = Graph()
    yield g
    output_file = Path(__file__).parent / "results/mvp_results.ttl"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=output_file, format="turtle")

def add_assessment_result(
        result_graph: Graph,
        subject: IdentifiedNode,
        assessment_type: URIRef,
        value: IdentifiedNode | Literal,
        assessment_date=None
):
    result_bn = BNode()
    result_graph.add((subject, DQAF.hasDQAFResult, result_bn))
    result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
    result_graph.add((result_bn, SDO.value, value))

    if assessment_date is None:
        assessment_date = datetime.now()
    elif isinstance(assessment_date, datetime.date) and not isinstance(assessment_date, datetime.datetime):
        assessment_date = datetime.datetime.combine(assessment_date, datetime.time.min)

    result_graph.add((result_bn, SOSA.resultTime, Literal(assessment_date, datatype=XSD.dateTime)))

