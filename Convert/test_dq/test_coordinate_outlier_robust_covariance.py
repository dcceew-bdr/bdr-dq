import folium
from pyoxigraph import Store
from Convert.rules.coordinate_outlier_robust_covariance import run_coordinate_outlier_robust_covariance
from Convert.test_data_generation.data_generation_coordinate_outlier_robust_covariance import create_coordinate_outlier_robust_covariance_test_data

def test_dq_coordinate_outlier_robust_covariance_map():
    # Create RDF test data with normal and outlier coordinates
    turtle_data = create_coordinate_outlier_robust_covariance_test_data()

    # Load the RDF data into a PyOxigraph store
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Run the robust covariance method to detect outlier coordinates
    run_coordinate_outlier_robust_covariance(store)

    # SPARQL query to get results and coordinates
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>
    PREFIX geo: <http://www.opengis.net/geosparql#>

    SELECT ?observation ?wkt ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_outlier_robust_covariance/> ;
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

    # Create a base map centered in Australia
    m = folium.Map(location=[-31, 152], zoom_start=5)

    # Add each observation as a circle marker
    for row in results:
        obs = str(row["observation"]).strip("<>")
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

    # Save the map to an HTML file in the current folder
    m.save("test_dq_coordinate_outlier_robust_covariance_map.html")
    print("Map saved: test_dq_coordinate_outlier_robust_covariance_map.html")

# Run this test if the script is executed directly
if __name__ == "__main__":
    test_dq_coordinate_outlier_robust_covariance_map()
