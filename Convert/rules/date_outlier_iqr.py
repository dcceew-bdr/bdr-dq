from pyoxigraph import Store
import numpy as np
from datetime import datetime

def run_date_outlier_iqr(store: Store):
    """
    This function checks if the observation date is very different (outlier).
    It uses IQR method and writes results into dqaf:fullResults graph.
    """

    # Step 1: Get all observation dates
    date_query = """
    PREFIX tern: <https://w3id.org/tern/ontologies/tern/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?observation ?dateVal
    WHERE {
      ?observation a tern:Observation ;
                   sosa:resultTime ?dateVal .
    }
    """
    results = list(store.query(date_query))

    # Step 2: Convert date string to timestamp (number)
    date_vals = []
    obs_map = {}
    for row in results:
        date_str = row["dateVal"].value  # example: "2022-03-01T00:00:00"
        date_obj = datetime.fromisoformat(date_str)
        timestamp = date_obj.timestamp()
        obs_uri = str(row["observation"]).strip("<>")
        date_vals.append(timestamp)
        obs_map[obs_uri] = timestamp

    # Step 3: Use IQR method to find outliers
    arr = np.array(date_vals)
    q1, q3 = np.percentile(arr, [25, 75])
    iqr = q3 - q1

    def is_outlier(val):
        return val < q1 - 1.5 * iqr or val > q3 + 1.5 * iqr

    # Step 4: Write the results using SPARQL INSERT
    insert_prefix = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    INSERT {
      GRAPH dqaf:fullResults {
    """
    insert_values = ""
    for obs_uri, ts in obs_map.items():
        tag = "outlier_date" if is_outlier(ts) else "normal_date"
        insert_values += f"""
        <{obs_uri}> dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/date_outlier_iqr/> ;
          schema:value "{tag}"
        ] .
        """

    insert_suffix = """
      }
    } WHERE { }
    """
    full_insert = insert_prefix + insert_values + insert_suffix
    store.update(full_insert)
