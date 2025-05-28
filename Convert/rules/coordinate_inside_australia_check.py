from pyoxigraph import Store

def run_coordinate_inside_australia_check(store: Store):
    """
    Check if coordinates are inside Australia.
    Marks each observation with "inside_australia" or "outside_australia".
    """

    # Step 1: Extract longitude and latitude values from WKT
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

    # Step 2: Store coordinates in a dictionary
    obs_map = {}
    for row in results:
        obs_uri = str(row["observation"]).strip("<>")
        lon = float(row["lonVal"].value)
        lat = float(row["latVal"].value)
        obs_map[obs_uri] = (lon, lat)

    # Step 3: Define Australia's bounding box
    def is_in_australia(lon, lat):
        return 112.0 <= lon <= 154.0 and -44.0 <= lat <= -10.0

    # Step 4: Prepare SPARQL INSERT query for tagging results
    insert_prefix = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    INSERT {
      GRAPH dqaf:fullResults {
    """
    insert_values = ""
    for obs_uri, (lon, lat) in obs_map.items():
        tag = "inside_australia" if is_in_australia(lon, lat) else "outside_australia"
        insert_values += f"""
        <{obs_uri}> dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_in_australia/> ;
          schema:value "{tag}"
        ] .
        """

    insert_suffix = """
      }
    } WHERE { }
    """
    full_query = insert_prefix + insert_values + insert_suffix

    # Step 5: Save the results into the RDF store
    store.update(full_query)
