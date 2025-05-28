from pyoxigraph import Store

from Convert.rules.date_outlier_iqr import run_date_outlier_iqr
from Convert.test_data_generation.data_generation_date_outlier_iqr_kmeans import create_date_outlier_iqr_test_data

def test_date_outlier_iqr():
    # Step 1: Create test RDF data (with normal and outlier dates)
    turtle_data = create_date_outlier_iqr_test_data()

    # Step 2: Load the RDF data into memory (PyOxigraph store)
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Step 3: Run the IQR rule to detect outlier dates
    run_date_outlier_iqr(store)

    # Step 4: Ask RDF for the result of the detection
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/date_outlier_iqr/> ;
          schema:value ?value
        ] .
      }
    }
    """

    results = store.query(query)

    # Step 5: Show the result on screen
    print("=== Date Outlier Detection Results ===")
    for row in results:
        print(f"{row['observation']} => {row['value'].value}")

# Optional: add this block to run manually
if __name__ == "__main__":
    test_date_outlier_iqr()
