import folium
from pyoxigraph import Store
from Convert.rules.coordinate_outlier_iqr import run_coordinate_outlier_iqr
from Convert.test_data_generation.data_generation_coordinate_outlier_iqr import create_coordinate_outlier_iqr_test_data

def test_coordinate_outlier_iqr_map():
    # Step 1: Generate RDF data
    turtle_data = create_coordinate_outlier_iqr_test_data()

    # Step 2: Load into Oxigraph store
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Step 3: Run IQR outlier detection
    run_coordinate_outlier_iqr(store)

    # Step 4: SPARQL query results
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>

    SELECT ?observation ?wkt ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_outlier_iqr/> ;
          schema:value ?value
        ] .
      }
      ?observation sosa:hasFeatureOfInterest ?sample .
      ?sample sosa:isResultOf ?procedure .
      ?procedure geo:hasGeometry ?geometry .
      ?geometry geo:asWKT ?wkt .
    }
    """
    results = store.query(query)

    # Step 5: Create map
    m = folium.Map(location=[-31, 152], zoom_start=5)

    for row in results:
        wkt = row["wkt"].value.replace("POINT(", "").replace(")", "")
        lon, lat = map(float, wkt.split())
        value = row["value"].value

        color = "green" if value == "normal_coordinate" else "red"

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=value
        ).add_to(m)

    # Step 6: Save map with specified name
    m.save("test_dq_coordinate_outlier_iqr.html")
    print("Map saved: test_dq_coordinate_outlier_iqr.html")

if __name__ == "__main__":
    test_coordinate_outlier_iqr_map()

