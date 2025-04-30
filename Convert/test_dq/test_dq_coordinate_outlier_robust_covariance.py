import folium
import pandas as pd
from pyoxigraph import Store
from Convert.rules.coordinate_outlier_robust_covariance import run_coordinate_outlier_robust_covariance
from Convert.test_data_generation.data_generation_coordinate_outlier_robust_covariance import create_coordinate_outlier_robust_covariance_test_data

def test_coordinate_outlier_robust_covariance_map():
    # === Step 1: Generate and load test RDF data ===
    turtle_data = create_coordinate_outlier_robust_covariance_test_data()
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Run Robust Covariance rule to classify coordinates ===
    run_coordinate_outlier_robust_covariance(store)

    # === Step 3: Query results and WKT points ===
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

    data = []
    for row in results:
        obs = str(row["observation"]).strip("<>")
        wkt = row["wkt"].value.replace("POINT(", "").replace(")", "")
        lon, lat = map(float, wkt.split())
        actual = row["value"].value

        expected = "outlier_coordinate" if int(obs.split("_")[-1]) >= 190 else "normal_coordinate"
        status = "match" if actual == expected else "mismatch"

        data.append({
            "observation": obs,
            "lon": lon,
            "lat": lat,
            "expected": expected,
            "actual": actual,
            "status": status
        })

    # === Step 4: Draw map ===
    m = folium.Map(location=[-36, 145], zoom_start=6)

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
            popup=folium.Popup(f"{d['observation']}<br>Expected: {d['expected']}<br>Actual: {d['actual']}")
        ).add_to(m)

    m.save("coordinate_outliers_robust_covariance_map.html")
    print("✅ Map saved as 'coordinate_outliers_robust_covariance_map.html'")
    print(pd.DataFrame(data).head())

if __name__ == "__main__":
    test_coordinate_outlier_robust_covariance_map()
