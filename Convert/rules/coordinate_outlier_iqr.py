from pyoxigraph import Store
import numpy as np

def run_coordinate_outlier_iqr(store: Store):
    """
    This function calculates coordinate outliers using the IQR method
    and writes the result back into dqaf:fullResults using INSERT/WHERE pattern.
    """

    # === Step 1: Query coordinates for all observations ===
    coord_query = """
    PREFIX tern: <https://w3id.org/tern/ontologies/tern/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
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

    # === Step 2: Prepare data for IQR calculation ===
    coords = []
    obs_map = {}
    for row in results:
        lon = float(row["lonVal"].value)
        lat = float(row["latVal"].value)
        obs_uri = str(row["observation"]).strip("<>")
        coords.append((lon, lat))
        obs_map[obs_uri] = (lon, lat)

    # === Step 3: Calculate IQR for lon and lat separately ===
    lons = np.array([pt[0] for pt in coords])
    lats = np.array([pt[1] for pt in coords])

    def is_outlier(val, q1, q3, iqr):
        return val < q1 - 1.5 * iqr or val > q3 + 1.5 * iqr

    lon_q1, lon_q3 = np.percentile(lons, [25, 75])
    lat_q1, lat_q3 = np.percentile(lats, [25, 75])
    lon_iqr = lon_q3 - lon_q1
    lat_iqr = lat_q3 - lat_q1

    # === Step 4: Build batch INSERT SPARQL query (INSERT { GRAPH { ... } } WHERE {}) ===
    insert_prefix = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    INSERT {
      GRAPH dqaf:fullResults {
    """
    insert_values = ""
    for obs_uri, (lon, lat) in obs_map.items():
        tag = "outlier_coordinate" if (
            is_outlier(lon, lon_q1, lon_q3, lon_iqr) or
            is_outlier(lat, lat_q1, lat_q3, lat_iqr)
        ) else "normal_coordinate"

        insert_values += f"""
        <{obs_uri}> dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_outlier_iqr/> ;
          schema:value "{tag}"
        ] .
        """

    insert_suffix = """
      }
    } WHERE { }
    """

    full_insert_query = insert_prefix + insert_values + insert_suffix

    # === Step 5: Run the SPARQL update ===
    store.update(full_insert_query)
