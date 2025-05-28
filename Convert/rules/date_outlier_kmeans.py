from pyoxigraph import Store
from datetime import datetime
import numpy as np
from sklearn.cluster import KMeans

def run_date_outlier_kmeans(store: Store, n_clusters=2):
    """
    This function checks if a date is unusual (outlier) using K-means clustering.
    Dates in the smallest group are called outliers. It writes the result into dqaf:fullResults.
    """

    # Step 1: Get resultTime (date) for each observation
    date_query = """
    PREFIX tern: <https://w3id.org/tern/ontologies/tern/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>

    SELECT ?observation ?dateVal
    WHERE {
      ?observation a tern:Observation ;
                   sosa:resultTime ?dateVal .
    }
    """
    results = list(store.query(date_query))

    # If not enough points, we skip
    if len(results) < n_clusters:
        return

    # Step 2: Convert dates to timestamps (numbers for K-means)
    timestamps = []
    obs_map = {}
    for row in results:
        obs_uri = str(row["observation"]).strip("<>")
        date_str = row["dateVal"].value
        ts = datetime.fromisoformat(date_str).timestamp()
        timestamps.append([ts])  # K-means needs 2D
        obs_map[obs_uri] = ts

    timestamps = np.array(timestamps)

    # Step 3: Run K-means and find the largest group (normal dates)
    model = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    labels = model.fit_predict(timestamps)
    unique, counts = np.unique(labels, return_counts=True)
    densest_cluster = unique[np.argmax(counts)]  # the biggest cluster = normal

    # Step 4: Create SPARQL INSERT query to save results
    insert_prefix = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    INSERT {
      GRAPH dqaf:fullResults {
    """
    insert_values = ""
    for i, (obs_uri, ts) in enumerate(obs_map.items()):
        tag = "normal_date" if labels[i] == densest_cluster else "outlier_date"
        insert_values += f"""
        <{obs_uri}> dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/date_outlier_kmeans/> ;
          schema:value "{tag}"
        ] .
        """

    insert_suffix = """
      }
    } WHERE { }
    """

    # Step 5: Run the update to store the results
    full_query = insert_prefix + insert_values + insert_suffix
    store.update(full_query)
