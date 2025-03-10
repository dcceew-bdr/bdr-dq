from pyoxigraph import Store

def assess_date_recency():
    store = Store()
    data_file = "chunk_1.ttl"

    with open(data_file, "rb") as f:
        store.load(f, format="text/turtle")

    with open("queries/assess_date_recency.sparql", "r") as file:
        query = file.read()

    results = store.query(query)

    recent_20_years_count = 0
    outdated_20_years_count = 0

    print("\n=== Observations and Date Recency ===")
    for row in results:
        observation = str(row["observation"]).strip("<>")
        date_literal = row["date"]

        if date_literal is not None:
            year = int(date_literal.value)
            if year >= 1900:
                label = "recent_20_years"
                recent_20_years_count += 1
            else:
                label = "outdated_20_years"
                outdated_20_years_count += 1

            print(f"Observation: {observation}")
            print(f"Date: {year}")
            print(f"Date Recency Label: {label}")
            print("-----")

    print("\n=== Summary ===")
    print(f"Total 'recent_20_years': {recent_20_years_count}")
    print(f"Total 'outdated_20_years': {outdated_20_years_count}")

if __name__ == "__main__":
    assess_date_recency()
