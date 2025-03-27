import pytest
from pyoxigraph import Store
from Convert.test_data_generation.data_generation_date_recency import create_date_recency_test_data

def test_date_recency():
    """
    This function tests whether the date recency SPARQL query correctly assigns labels
    like "recent_20_years" or "outdated_20_years" based on the year in the observation data.

    It does this by:
    1. Creating RDF test data (3 observations).
    2. Loading that data into an in-memory RDF store (using PyOxigraph).
    3. Running the INSERT query to write the results into a special graph.
    4. Running a SELECT query to read the inserted results.
    5. Comparing the output with expected values.
    """

    # === Step 1: Generate RDF test data ===
    # This includes:
    # - observation1 (2022): should be labeled "recent_20_years"
    # - observation2 (1800): should be labeled "outdated_20_years"
    # - observation3: has no date and should be ignored
    turtle_data = create_date_recency_test_data()

    # Load the test data into an RDF store (in-memory triple store)
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Load and run the SPARQL INSERT query ===
    # This will calculate recency and insert the result into dqaf:fullResults graph
    query_path = "../queries/assess_date_recency.sparql"
    with open(query_path, "r") as f:
        insert_query = f.read()
    store.update(insert_query)  # Important: use .update() instead of .query() for INSERT

    # === Step 3: SELECT query to get the results that were inserted ===
    select_query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/date_recency/> ;
          schema:value ?value
        ]
      }
    }
    """
    results = store.query(select_query)

    # === Step 4: Convert query results into Python dictionary ===
    # Format: { observation_uri: result_value }
    actual_results = {
        str(row["observation"]).strip("<>"): row["value"].value
        for row in results
    }

    print("\nExtracted Results:", actual_results)

    # === Step 5: Define what results we expect based on test data ===
    expected_results = {
        "https://w3id.org/tern/ontologies/tern/observation1": "recent_20_years",
        "https://w3id.org/tern/ontologies/tern/observation2": "outdated_20_years"
    }

    # === Step 6: Compare actual results with expected values ===
    # If any observation is missing or incorrectly labeled, the test will fail
    for obs_uri, expected_value in expected_results.items():
        assert obs_uri in actual_results, f"Missing observation: {obs_uri}"
        assert actual_results[obs_uri] == expected_value, \
            f"Expected: {expected_value}, Got: {actual_results[obs_uri]}"
