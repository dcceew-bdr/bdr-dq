import pytest
import os
from pyoxigraph import Store

@pytest.fixture
def test_graph():
    store = Store()
    data_file = "test_data.ttl"

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"File {data_file} not found.")

    with open(data_file, "rb") as f:
        store.load(f, format="text/turtle")

    return store

@pytest.fixture
def query():
    with open("queries/assess_date_recency.sparql", "r") as file:
        return file.read()

def test_date_recency_check(test_graph, query):
    results = test_graph.query(query)
    extracted_results = {str(row["observation"]).strip("<>"): int(row["date"].value) for row in results if row["date"] is not None}

    assert "https://w3id.org/tern/ontologies/tern/observation1" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation1"] >= 2000

    assert "https://w3id.org/tern/ontologies/tern/observation2" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation2"] < 1900

    assert "https://w3id.org/tern/ontologies/tern/observation3" not in extracted_results
