import pytest
from pyoxigraph import Store

from Convert.test_data_generation.data_generation_date_recency import create_test_graph


def test_date_recency_check():
    """
    Steps in this test:
    1. Generate RDF test data using `create_test_graph()`.
    2. Load the RDF data into an in-memory RDF store.
    3. Load and run the SPARQL query that checks if observations are recent or outdated.
    4. Extract the results and check if they match expected values.
    """

    # === Step 1: Generate and load RDF test data ===
    turtle_data = create_test_graph()  # Get the RDF data in Turtle format

    # Create an RDF store (storage system for the test data)
    store = Store()

    # Load the generated RDF data directly into the store
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Load the SPARQL query ===
    query_file = "../queries/assess_date_recency.sparql"

    try:
        with open(query_file, "r") as file:
            query = file.read()
    except FileNotFoundError:
        pytest.fail(f"SPARQL query file {query_file} not found.")

    # === Step 3: Run the query on the RDF store ===
    results = store.query(query)

    # === Step 4: Extract results from the query ===
    extracted_results = {
        str(row["observation"]).strip("<>"): row["is_recent"].value
        for row in results if row["is_recent"] is not None
    }

    # Print extracted results for debugging.
    print("\nExtracted Results from SPARQL Query:", extracted_results)

    # === Step 5: Verify only requested test cases using `is_recent` ===

    # Observation2 (1800) should be classified as "outdated_20_years".
    assert "https://w3id.org/tern/ontologies/tern/observation2" in extracted_results, \
        f"Observation2 missing. Extracted results: {extracted_results}"
    assert extracted_results["https://w3id.org/tern/ontologies/tern/observation2"] == "outdated_20_years", \
        f"Observation2 incorrectly classified. Extracted results: {extracted_results}"

    # Observation3 has no date and should not appear in the results.
    assert "https://w3id.org/tern/ontologies/tern/observation3" not in extracted_results, \
        f"Observation3 should not be present but found: {extracted_results}"
