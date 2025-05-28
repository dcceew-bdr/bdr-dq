from pyoxigraph import Store
import numpy as np
from sklearn.covariance import MinCovDet

def run_coordinate_outlier_robust_covariance(store: Store, threshold: float = 5.0):
    """
    Detect outlier coordinates using Robust Covariance method (Mahalanobis distance).
    Add results into RDF store using SPARQL INSERT statement.
    """

    # Step 1: Get longitude and latitude from WKT geometry
    coord_query = """
    PREFIX tern: <https://w3id.org/tern/ontologies/tern/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/geosparql#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?observation ?lonVal ?latVal
    WHERE {
      ?observation a tern:Observation ;
                   sosa:hasFeatureOfInterest ?sample .
      ?sample a tern:Sample ;
              sosa:isResultOf ?procedure .
      ?procedure geo:hasGeometry ?geometry .
      ?geometry geo:asWKT ?wkt .

      BIND(STR(?wkt) AS ?wktStr)
      BIND(STRBEFORE(STRAFTER(?wktStr, "POINT("), ")") AS ?coordStr)
      BIND(STRBEFORE(?coordStr, " ") AS ?lonStr)
      BIND(STRAFTER(?coordStr, " ") AS ?latStr)
      BIND(xsd:float(?lonStr) AS ?lonVal)
      BIND(xsd:float(?latStr) AS ?latVal)
    }
    """
    results = list(store.query(coord_query))

    # Step 2: Check if we got any coordinates
    if not results:
        print("⚠️ No coordinates found.")
        return

    coords = []
    obs_map = {}  # Keep track of which coordinates belong to which observation
    for row in results:
        lon = float(row["lonVal"].value)
        lat = float(row["latVal"].value)
        obs_uri = str(row["observation"]).strip("<>")
        coords.append([lon, lat])
        obs_map[obs_uri] = (lon, lat)

    coords = np.array(coords)

    # Step 3: Use Robust Covariance to calculate Mahalanobis distances
    robust_cov = MinCovDet().fit(coords)
    distances = robust_cov.mahalanobis(coords)

    # Step 4: Create SPARQL INSERT query to add outlier results to RDF
    insert_prefix = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    INSERT {
      GRAPH dqaf:fullResults {
    """
    insert_values = ""
    for obs_uri, dist in zip(obs_map.keys(), distances):
        tag = "outlier_coordinate" if dist > threshold else "normal_coordinate"
        insert_values += f"""
        <{obs_uri}> dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_outlier_robust_covariance/> ;
          schema:value "{tag}"
        ] .
        """

    insert_suffix = """
      }
    } WHERE { }
    """
    full_insert_query = insert_prefix + insert_values + insert_suffix

    # Step 5: Save results to RDF store
    store.update(full_insert_query)
