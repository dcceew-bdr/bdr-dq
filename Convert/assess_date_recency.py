# This script evaluates the recency of observation records based on their dates.
# It categorizes each observation as either "recent" (within the last 20 years) or "outdated" (older than 20 years).

from pyoxigraph import Store


def assess_date_recency():
    # Create an RDF store to load and process data.
    store = Store()
    data_file = "chunk_1.ttl"  # Input data file containing observations.

    # Load the RDF data from the file.
    with open(data_file, "rb") as f:
        store.load(f, format="text/turtle")

    # Read the SPARQL query that evaluates date recency.
    with open("../../DQAF/queries/assess_date_recency.sparql", "r") as file:
        query = file.read()

    # Run the query on the loaded data.
    results = store.query(query)

    # Counters for observations classified as recent or outdated.
    recent_20_years_count = 0
    outdated_20_years_count = 0

    print("\n=== Observations and Date Recency ===")

    # Process each observation in the query results.
    for row in results:
        observation = str(row["observation"]).strip("<>")  # Extract observation ID.
        date_literal = row["date"]  # Extract the observation date.

        if date_literal is not None:
            year = int(date_literal.value)  # Convert the date to an integer year.

            # Categorize the observation as recent or outdated.
            if year >= 1900:
                label = "recent_20_years"
                recent_20_years_count += 1
            else:
                label = "outdated_20_years"
                outdated_20_years_count += 1

            # Print the observation details.
            print(f"Observation: {observation}")
            print(f"Date: {year}")
            print(f"Date Recency Label: {label}")
            print("-----")

    # Print a summary of the results.
    print("\n=== Summary ===")
    print(f"Total 'recent_20_years': {recent_20_years_count}")
    print(f"Total 'outdated_20_years': {outdated_20_years_count}")


# Execute the function if the script is run directly.
if __name__ == "__main__":
    assess_date_recency()
