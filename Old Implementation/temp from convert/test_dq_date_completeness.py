# This script checks if the SPARQL query correctly identifies whether observations have a date (date completeness check).

import pytest  # Import pytest for testing
import os  # Import os to check if files exist
from pyoxigraph import Store  # Import Store to handle RDF data

def test_date_completeness_check():
    """
    This test_dq follows these steps:
    1. Load the RDF test_dq data (dataset of observations).
    2. Load and run the SPARQL query that checks if observations have dates.
    3. Extract the results and check if they match the expected values.
    """

    # === Step 1: Load the RDF test_dq data ===
    data_file = "test_data/test_data_date_completeness.ttl"  # File with test_dq data

    # Check if the test_dq data file exists; if not, stop the test_dq.
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Error: Test data file '{data_file}' not found.")

    # Create an RDF store (like a small database to hold the data)
    store = Store()

    # Open the RDF file and load it into the store.
    with open(data_file, "rb") as f:
        store.load(f, format="text/turtle")  # Load data in Turtle format

    # Print all RDF data for debugging (optional)
    print("\n=== RDF Data Loaded ===")
    for triple in store:
        print(triple)  # Show each data entry in the dataset

    # === Step 2: Load the SPARQL query ===
    query_file = "../../Convert/queries/assess_date_completeness.sparql"  # File containing the SPARQL query

    # Check if the SPARQL query file exists; if not, stop the test_dq.
    if not os.path.exists(query_file):
        raise FileNotFoundError(f"Error: SPARQL query file '{query_file}' not found.")

    # Open the query file and read its content.
    with open(query_file, "r") as file:
        query = file.read()

    # === Step 3: Run the query on the test_dq RDF data ===
    results = store.query(query)

    # === Step 4: Extract results from the query ===
    # Get the observation ID and its completeness status (empty or non_empty).
    extracted_results = {
        str(row["observation"]).strip("<>"): row["assess_date_completeness"].value
        for row in results if "assess_date_completeness" in row
    }

    # Print extracted results for debugging (optional)
    print("\n=== Extracted Results from SPARQL Query ===")
    print(extracted_results)

    # === Step 5: Verify the test_dq results ===

    # Expected results based on test_dq data:
    expected_results = {
        "http://createme.org/observation/scientificName/obs_with_date": "non_empty",  # Has a date
        "http://createme.org/observation/scientificName/obs_no_date": "empty",  # No date
        "http://createme.org/observation/scientificName/obs_missing_date": "empty",  # Time reference but no date
    }

    # Compare expected results with extracted results
    for obs, expected_value in expected_results.items():
        assert obs in extracted_results, f"Error: {obs} is missing. Extracted results: {extracted_results}"
        assert extracted_results[obs] == expected_value, \
            f"Error: Mismatch for {obs}. Expected: {expected_value}, Got: {extracted_results.get(obs, 'MISSING')}"
