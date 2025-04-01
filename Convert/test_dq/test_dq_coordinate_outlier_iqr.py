import folium
import pandas as pd
from pyoxigraph import Store
from Convert.rules.coordinate_outlier_iqr import run_coordinate_outlier_iqr
from Convert.test_data_generation.data_generation_coordinate_outlier_iqr import create_coordinate_outlier_iqr_test_data

def test_coordinate_outlier_iqr_map():
    # === Step 1: Generate and load test RDF data ===
    turtle_data = create_coordinate_outlier_iqr_test_data()
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Run IQR rule to classify coordinates ===
    run_coordinate_outlier_iqr(store)

    # === Step 3: Query results and WKT points ===
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

    # === Step 4: Build result table and guess expected classification from ID ===
    data = []
    for row in results:
        obs = str(row["observation"]).strip("<>")
        wkt = row["wkt"].value.replace("POINT(", "").replace(")", "")
        lon, lat = map(float, wkt.split())
        actual = row["value"].value

        # Infer expected label based on naming (you can adjust this logic)
        if "obs_manual_3" in obs or "obs_manual_4" in obs or int(obs.split("_")[-1]) >= 190:
            expected = "outlier_coordinate"
        else:
            expected = "normal_coordinate"

        status = "match" if actual == expected else "mismatch"

        data.append({
            "observation": obs,
            "lon": lon,
            "lat": lat,
            "expected": expected,
            "actual": actual,
            "status": status
        })

    # === Step 5: Draw map with folium ===
    m = folium.Map(location=[-35, 145], zoom_start=5)

    for d in data:
        if d["status"] == "mismatch":
            color = "yellow"
        elif d["actual"] == "outlier_coordinate":
            color = "red"
        else:
            color = "green"

        folium.CircleMarker(
            location=[d["lat"], d["lon"]],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(
                f"<b>{d['observation']}</b><br>Expected: {d['expected']}<br>Actual: {d['actual']}",
                max_width=250
            )
        ).add_to(m)

    m.save("coordinate_outliers_comparison_map.html")
    print("✅ Map saved as 'coordinate_outliers_comparison_map.html'")
    print(pd.DataFrame(data).head())

# Run manually
if __name__ == "__main__":
    test_coordinate_outlier_iqr_map()
