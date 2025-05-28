import folium
from pyoxigraph import Store
from Convert.rules.coordinate_outlier_zscore import run_coordinate_outlier_zscore
from Convert.test_data_generation.data_generation_coordinate_outlier_zscore import create_coordinate_outlier_zscore_test_data

def test_dq_coordinate_outlier_zscore_map():
    # Step 1: Create RDF data with normal and outlier coordinates
    turtle_data = create_coordinate_outlier_zscore_test_data()

    # Step 2: Load RDF data into PyOxigraph store
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Step 3: Apply the Z-score detection method
    run_coordinate_outlier_zscore(store)

    # Step 4: Query RDF to get result label and coordinate
    query = """
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>
    PREFIX geo: <http://www.opengis.net/geosparql#>

    SELECT ?observation ?wkt ?value
    WHERE {
      GRAPH dqaf:fullResults {
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/coordinate_outlier_zscore/> ;
          schema:value ?value
        ] .
      }
      ?observation sosa:hasFeatureOfInterest ?sample .
      ?sample sosa:isResultOf ?procedure .
      ?procedure geo:hasGeometry ?geometry .
      ?geometry geo:asWKT ?wkt .
    }
    """
    results = list(store.query(query))

    # Step 5: Create the map with default zoom on Victoria, Australia
    m = folium.Map(location=[-36, 145], zoom_start=6)

    # Step 6: Draw each point on the map
    for row in results:
        wkt = row["wkt"].value.replace("POINT(", "").replace(")", "")
        lon, lat = map(float, wkt.split())
        label = row["value"].value

        # Choose red for outliers, green for normal points
        color = "green" if label == "normal_coordinate" else "red"

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=label
        ).add_to(m)

    # Step 7: Save the map to a local HTML file
    m.save("test_dq_coordinate_outlier_zscore_map.html")
    print("Map saved: test_dq_coordinate_outlier_zscore_map.html")

# Only run this if the file is executed directly
if __name__ == "__main__":
    test_dq_coordinate_outlier_zscore_map()
