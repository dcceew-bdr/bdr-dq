import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
import folium

# Input/output paths
TRAINING_PATH = "../test_data_generation/training_coordinates.csv"
MODEL_PATH = "isolation_forest_model.pkl"
MAP_PATH = "training_data_outlier_map.html"

def train_model(input_csv=TRAINING_PATH, model_path=MODEL_PATH):
    df = pd.read_csv(input_csv)
    df["label"] = df["label"].astype(str).str.strip().str.upper()

    # === Step 1: Build semi-supervised training set ===
    df_N = df[df["label"] == "N"]
    df_unlabeled = df[~df["label"].isin(["N", "O"])]

    if len(df_N) == 0:
        print("No labeled normal points ('N') found. Using all data for training.")
        coords_train = df[["lon", "lat"]].values
    else:
        sample_unlabeled = df_unlabeled.sample(
            min(len(df_unlabeled), len(df_N)*2), random_state=42
        )
        train_df = pd.concat([df_N, sample_unlabeled], ignore_index=True)
        coords_train = train_df[["lon", "lat"]].values
        print(f"Training on {len(df_N)} 'N' points + {len(sample_unlabeled)} sampled unlabeled points.")

    # === Train the model ===
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(coords_train)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # === Step 2: Predict on all points ===
    coords_all = df[["lon", "lat"]].values
    preds = model.predict(coords_all)
    scores = model.decision_function(coords_all)

    # === Step 3: Create map ===
    avg_lat = df["lat"].mean()
    avg_lon = df["lon"].mean()
    fmap = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

    # Define score thresholds for coloring
    q10 = pd.Series(scores).quantile(0.0002)
    q03 = pd.Series(scores).quantile(0.0001)

    for i, row in df.iterrows():
        lat, lon = row["lat"], row["lon"]
        name = row.get("name", f"obs{i+1}")
        label = row["label"]
        score = scores[i]

        # Color assignment logic
        if label == "N":
            point_type = "human_normal"
            color = "green"
        elif label == "O":
            point_type = "human_outlier"
            color = "red"
        else:
            if preds[i] == 1:
                point_type = "model_normal"
                color = "green"
            else:
                point_type = "model_outlier"
                if score <= q03:
                    color = "red"     # Most extreme outliers
                else:
                    color = "orange"  # Less extreme outliers

        popup = f"{name}<br>{point_type}<br>Score: {score:.4f}"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup, max_width=300)
        ).add_to(fmap)

    fmap.save(MAP_PATH)
    print(f"Outlier map saved to {MAP_PATH}")

if __name__ == "__main__":
    train_model()
