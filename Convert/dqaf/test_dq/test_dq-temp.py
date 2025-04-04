import pytest
from pyoxigraph import Store
from Convert.test_data_generation.data_generation_coordinate_completeness import create_coordinate_completeness_test_data
from Convert.test_data_generation.data_generation_coordinate_precision import create_coordinate_precision_test_data

def test_coordinate_precision():
    # === Step 1: Generate RDF test data ===
    turtle_data = create_coordinate_precision_test_data()

    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Load the SPARQL query ===
    query_path = "../queries/assess_coordinate_precision.sparql"
    with open(query_path, "r") as f:
        query = f.read()

    # === Step 3: Run the query ===
    results = store.query(query)

    # === Step 4: Extract and map results
    actual_results = {}
    for row in results:
        obs = str(row["observation"]).strip("<>")
        val = row["coordinate_precision"].value
        actual_results[obs] = val

    print("\nExtracted Results:", actual_results)

    # === Step 5: Expected values ===
    expected_results = {
        "https://w3id.org/tern/ontologies/tern/obs_low_precision": "Low",
        "https://w3id.org/tern/ontologies/tern/obs_medium_precision": "Low",
        "https://w3id.org/tern/ontologies/tern/obs_high_precision": "Low"
    }

    # === Step 6: Assertions ===
    for obs_uri, expected_value in expected_results.items():
        assert obs_uri in actual_results, f"Missing observation: {obs_uri}"
        assert actual_results[obs_uri] == expected_value, \
            f"Expected: {expected_value}, Got: {actual_results[obs_uri]}"


def test_coordinate_completeness():
    # === Step 1: Generate RDF test data ===
    turtle_data = create_coordinate_completeness_test_data()

    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Load the SPARQL query ===
    query_path = "../queries/assess_coordinate_completeness.sparql"
    with open(query_path, "r") as f:
        query = f.read()

    # === Step 3: Run the query ===
    results = store.query(query)


    # === Step 4: Extract and map results
    actual_results = {}
    for row in results:
        obs = str(row["observation"]).strip("<>")
        val = row["assess_coordinate_completeness"].value
        actual_results[obs] = val

    print("\nExtracted Results:", actual_results)

    # === Step 5: Expected values ===
    expected_results = {
        "https://w3id.org/tern/ontologies/tern/obs_with_coordinates": "non_empty",
        "https://w3id.org/tern/ontologies/tern/obs_missing_coordinates": "empty"
    }

    # === Step 6: Assertions ===
    for obs_uri, expected_value in expected_results.items():
        assert obs_uri in actual_results, f"Missing observation: {obs_uri}"
        assert actual_results[obs_uri] == expected_value, \
            f"Expected: {expected_value}, Got: {actual_results[obs_uri]}"