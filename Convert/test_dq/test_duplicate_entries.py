from pyoxigraph import Store
from Convert.test_data_generation.data_generation_duplicate_entries import create_duplicate_test_data

def test_duplicate_entries():
    # Step 1: Create RDF memory store
    store = Store()

    # Step 2: Create RDF test data (some are duplicate)
    ttl = create_duplicate_test_data()
    store.load(ttl.encode("utf-8"), format="text/turtle")

    # Step 3: Run SPARQL rule to check duplicate values
    with open("../queries/assess_duplicate_entries.sparql", "r") as f:
        store.update(f.read())

    # Step 4: Ask for results from dqaf:fullResults graph
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/duplicate/> ;
          schema:value ?value
        ] .
      }
    }
    """
    results = store.query(query)

    # Step 5: Turn SPARQL results into Python dictionary
    actual = {
        str(row["observation"]).strip("<>"): row["value"].value
        for row in results
    }

    # Step 6: Expected values (we know which ones are duplicates)
    expected = {
        "http://example.com/test/obs1": "duplicate_entry",
        "http://example.com/test/obs2": "duplicate_entry",
        "http://example.com/test/obs3": "unique_entry"
    }

    # Step 7: Print result
    print("\n=== Duplicate Entry Detection ===")
    for k, v in actual.items():
        print(f"{k} => {v}")

    # Step 8: Check if the actual results match what we expect
    for obs_uri, expected_val in expected.items():
        assert obs_uri in actual, f"Missing: {obs_uri}"
        assert actual[obs_uri] == expected_val, \
            f"Expected: {expected_val}, Got: {actual[obs_uri]}"
