import joblib
import re
import numpy as np
import folium
from pyoxigraph import Store, RdfFormat, NamedNode, Literal, Quad
import sys
import os

from Convert.test_data_generation.data_generation_coordinate_outlier_isolation_forest_test import \
    create_coordinate_outlier_isolation_forest_test_data

# RDF base namespaces
DQAF_BASE = "http://example.com/def/dqaf/"
SOSA_BASE = "http://www.w3.org/ns/sosa/"
GEO_BASE = "http://www.opengis.net/geosparql#"
SCHEMA_BASE = "http://schema.org/"
ASSESS = NamedNode("http://example.com/assess/coordinate_outlier_isolation_forest/")
FULL_RESULTS = NamedNode(DQAF_BASE + "fullResults")

# Make full URI
def uri(namespace: str, suffix: str) -> NamedNode:
    return NamedNode(namespace + suffix)

# Load model and detect outliers from RDF coordinates
def run_coordinate_outlier_isolation_forest(store: Store, model_path=None):
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), "isolation_forest_model.pkl")

    print(f"Loading model from: {model_path}")
    model = joblib.load(model_path)

    # SPARQL to get coordinates
    query = """
    PREFIX geo: <http://www.opengis.net/geosparql#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>

    SELECT ?observation ?wkt
    WHERE {
      ?observation sosa:hasFeatureOfInterest ?sample .
      ?sample sosa:isResultOf ?procedure .
      ?procedure geo:hasGeometry ?geometry .
      ?geometry geo:asWKT ?wkt .
    }
    """
    results = store.query(query)

    coords = []
    obs_ids = []

    for row in results:
        obs_ids.append(row["observation"])
        match = re.search(r"POINT\s*\(\s*([\d\.-]+)\s+([\d\.-]+)\s*\)", row["wkt"].value)
        if match:
            lon, lat = float(match.group(1)), float(match.group(2))
            coords.append([lon, lat])

    if not coords:
        print("No coordinates found.")
        return []

    coords_np = np.array(coords)
    preds = model.predict(coords_np)             # 1 = normal, -1 = outlier
    scores = model.decision_function(coords_np)  # smaller = more likely outlier

    results_with_locations = []
    for i, (obs, pred, coord, score) in enumerate(zip(obs_ids, preds, coords, scores)):
        result_uri = NamedNode(f"http://example.com/result/{i}")
        value_str = "outlier_coordinate" if pred == -1 else "normal_coordinate"
        value = Literal(value_str)
        lat, lon = coord[1], coord[0]

        store.add(Quad(obs, uri(DQAF_BASE, "hasResult"), result_uri, FULL_RESULTS))
        store.add(Quad(result_uri, uri(SOSA_BASE, "observedProperty"), ASSESS, FULL_RESULTS))
        store.add(Quad(result_uri, uri(SCHEMA_BASE, "value"), value, FULL_RESULTS))

        results_with_locations.append((lat, lon, value_str, score))

    return results_with_locations

# Run when this file is executed directly
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_data_generation")))

    turtle_data = create_coordinate_outlier_isolation_forest_test_data()
    store = Store()
    store.load(turtle_data.encode("utf-8"), RdfFormat.TURTLE)

    results_with_locations = run_coordinate_outlier_isolation_forest(store)

    print("Outlier detection results:")
    for _, _, label, score in results_with_locations:
        print(f"- \"{label}\" | Score: {score:.6f}")

    if results_with_locations:
        avg_lat = sum(lat for lat, _, _, _ in results_with_locations) / len(results_with_locations)
        avg_lon = sum(lon for _, lon, _, _ in results_with_locations) / len(results_with_locations)
        fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

        for lat, lon, label, score in results_with_locations:
            color = "red" if label == "outlier_coordinate" else "green"
            popup_text = f"{label}<br>Lat: {lat:.6f}, Lon: {lon:.6f}<br>Score: {score:.6f}"

            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(fmap)

        map_path = os.path.join(os.path.dirname(__file__), "coordinate_outliers_isolation_forest_map.html")
        fmap.save(map_path)
        print(f"Map with scores saved to '{map_path}'")
    else:
        print("No data available to show on map.")
