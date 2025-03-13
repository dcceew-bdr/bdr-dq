# This script tests the date recency evaluation function.

import pytest
import os
from pyoxigraph import Store


@pytest.fixture
def test_graph():
    # Create an RDF store to load and process test data.
    store = Store()
    data_file = "test_data.ttl"

    # Ensure the test data file exists before loading.
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"File {data_file} not found.")

    # Load the RDF data from the test file.
    with open(data_file, "rb") as f:
        store.load(f, format="text/turtle")

    return store


@pytest.fixture
def query():
    # Load the SPARQL query that checks the date recency of observations.
    with open("../../DQAF/queries/assess_date_recency.sparql", "r") as file:
        return file.read()


def test_date_recency_check(test_graph, query):
    # Run the query on the test RDF graph.
    results = test_graph.query(query)

    # Extract the observation ID and its associated year from the query results.
    extracted_results = {str(row["observation"]).strip("<>"): int(row["date"].value) for row in results if
                         row["date"] is not None}

    # Verify that observation1 is categorized as recent (after 2000).
    assert "https://w3id.org/tern/ontologies/tern/observation1" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation1"] >= 2000

    # Verify that observation2 is categorized as outdated (before 1900).
    assert "https://w3id.org/tern/ontologies/tern/observation2" in extracted_results
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation2"] < 1900

    # Verify that observation3, which has no date, is not included in the results.
    assert "https://w3id.org/tern/ontologies/tern/observation3" not in extracted_results
