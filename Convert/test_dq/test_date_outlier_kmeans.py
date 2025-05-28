from pyoxigraph import Store
from Convert.rules.date_outlier_kmeans import run_date_outlier_kmeans
from Convert.test_data_generation.data_generation_date_outlier_iqr_kmeans import create_date_outlier_iqr_test_data

def test_date_outlier_kmeans():
    # Step 1: Make test RDF data with some normal and outlier dates
    turtle_data = create_date_outlier_iqr_test_data()

    # Step 2: Load the RDF data into memory using PyOxigraph store
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Step 3: Run the K-means rule to find outlier dates
    run_date_outlier_kmeans(store)

    # Step 4: Ask RDF graph for result values
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/date_outlier_kmeans/> ;
          schema:value ?value
        ] .
      }
    }
    """
    results = store.query(query)

    # Step 5: Print the result on screen
    print("=== Date Outlier K-means Detection Results ===")
    for row in results:
        print(f"{row['observation']} => {row['value'].value}")

# Run this script directly
if __name__ == "__main__":
    test_date_outlier_kmeans()
