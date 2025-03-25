import pytest
from pyoxigraph import Store
from Convert.test_data_generation.data_generation_date_recency import create_test_graph as create_recency_test_graph
from Convert.test_data_generation.data_generation_date_completeness import create_date_completeness_test_data


@pytest.mark.parametrize("query_file, generate_data_function, expected_results", [
    ("../queries/assess_date_recency.sparql", create_recency_test_graph, {
        "https://w3id.org/tern/ontologies/tern/observation1": "recent_20_years",
        "https://w3id.org/tern/ontologies/tern/observation2": "outdated_20_years"
    }),
    ("../queries/assess_date_completeness.sparql", create_date_completeness_test_data, {
        "http://createme.org/observation/scientificName/obs_with_date": "non_empty",
        "http://createme.org/observation/scientificName/obs_no_date": "empty",
        "http://createme.org/observation/scientificName/obs_missing_date": "empty"
    })
])
def test_dq_assessments(query_file, generate_data_function, expected_results):
    """
    Generic test function to assess multiple SPARQL queries on generated RDF test data.
    """

    # === Step 1: Generate RDF test data ===
    turtle_data = generate_data_function()  # Get the RDF data in Turtle format

    # Create an RDF store (storage system for the test data)
    store = Store()

    # Load the generated RDF data directly into the store
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Load the SPARQL query ===
    try:
        with open(query_file, "r") as file:
            query = file.read()
    except FileNotFoundError:
        pytest.fail(f"SPARQL query file {query_file} not found.")

    # === Step 3: Run the query on the RDF store ===
    results = store.query(query)

    # === Step 4: Extract results from the query ===
    extracted_results = {
        str(row["observation"]).strip("<>"): row["is_recent"].value if "is_recent" in row else row[
            "assess_date_completeness"].value
        for row in results if "is_recent" in row or "assess_date_completeness" in row
    }

    # Print extracted results for debugging.
    print(f"\nExtracted Results from {query_file}:", extracted_results)

    # === Step 5: Verify test results ===
    for obs, expected_value in expected_results.items():
        assert obs in extracted_results, f"Observation {obs} is missing. Extracted results: {extracted_results}"
        assert extracted_results[obs] == expected_value, \
            f"Observation {obs} incorrectly classified. Expected: {expected_value}, Got: {extracted_results.get(obs, 'MISSING')}"