from pyoxigraph import Store
from Convert.rules.coordinate_inside_australia_check import run_coordinate_inside_australia_check
from Convert.test_data_generation.data_generation_coordinate_outlier_iqr import create_coordinate_outlier_iqr_test_data

def test_coordinate_inside_australia():
    # Step 1: Create RDF test data with some points inside and outside Australia
    turtle_data = create_coordinate_outlier_iqr_test_data()

    # Step 2: Load RDF data into PyOxigraph store
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Step 3: Run the check function to decide if coordinates are inside Australia or not
    run_coordinate_inside_australia_check(store)

    # Step 4: Get the result from the RDF store using SPARQL
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_in_australia/> ;
          schema:value ?value
        ] .
      }
    }
    """
    results = store.query(query)

    # Step 5: Print all results to see which coordinates are inside or outside
    print("=== Coordinate Inside/Outside Australia ===")
    for row in results:
        print(f"{row['observation']} => {row['value'].value}")

# Run the test if this file is executed directly
if __name__ == "__main__":
    test_coordinate_inside_australia()
