import random
import csv

# File path for saving data
TRAINING_PATH = "training_coordinates.csv"

def generate_training_coordinates(filepath=TRAINING_PATH):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "lon", "lat", "label"])  # Header

        # === 100 points near Sydney ===
        for i in range(100):
            lon = round(151.2 + random.uniform(-0.05, 0.05), 6)
            lat = round(-33.9 + random.uniform(-0.05, 0.05), 6)
            name = f"obs{i+1}"
            writer.writerow([name, lon, lat, ""])

        # === 100 points near Queensland ===
        for i in range(100):
            lon = round(153.0 + random.uniform(-0.05, 0.05), 6)
            lat = round(-27.5 + random.uniform(-0.05, 0.05), 6)
            name = f"obs{100+i+1}"
            writer.writerow([name, lon, lat, ""])

        # === 10 random outliers ===
        for i in range(10):
            lon = round(random.uniform(140.0, 160.0), 6)
            lat = round(random.uniform(-40.0, -20.0), 6)
            name = f"obs{200+i+1}"
            writer.writerow([name, lon, lat, ""])

    print(f"Training data saved to: {filepath}")

# Run it directly
if __name__ == "__main__":
    generate_training_coordinates()
