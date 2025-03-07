from rdflib import Graph

def assess_date_recency():
    g = Graph()
    g.parse("chunk_1.ttl", format="turtle")

    with open("assess_date_recency.sparql", "r") as file:
        query = file.read()

    results = g.query(query)

    recent_20_years_count = 0
    outdated_20_years_count = 0

    for row in results:
        observation, date = row
        year = int(date)

        if year >= 1900:
            date_recency = "recent_20_years"
            recent_20_years_count += 1
        else:
            date_recency = "outdated_20_years"
            outdated_20_years_count += 1

        print(f"Observation: {observation}")
        print(f"Date: {year}")
        print(f"Date Recency: {date_recency}")
        print("-----")

    print("\n=== Summary ===")
    print(f"Total 'recent_20_years': {recent_20_years_count}")
    print(f"Total 'outdated_20_years': {outdated_20_years_count}")

if __name__ == "__main__":
    assess_date_recency()
