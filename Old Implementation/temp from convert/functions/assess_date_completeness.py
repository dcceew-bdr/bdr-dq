import os  # Import the module to work with files
from pyoxigraph import Store, RdfFormat  # Import RDF storage and format handling

def assess_date_completeness():
    """
    This function checks if observations in an RDF dataset have a date.
    It categorizes them as either "non_empty" (has a date) or "empty" (no date).
    """

    # Define the file paths for the dataset and the SPARQL query
    data_file = "../test_data/chunk_1.ttl"  # RDF dataset file (Turtle format)
    query_file = "../../../Convert/queries/assess_date_completeness.sparql"  # SPARQL query file

    # Check if the data file exists; if not, show an error and stop the program
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Error: Data file '{data_file}' not found.")

    # Create an RDF store (a database to hold RDF data)
    store = Store()

    # Load the RDF data from the file into the store
    with open(data_file, "rb") as f:
        store.load(f, format=RdfFormat.TURTLE)  # Load in Turtle format

    # Check if the SPARQL query file exists; if not, show an error and stop the program
    if not os.path.exists(query_file):
        raise FileNotFoundError(f"Error: SPARQL query file '{query_file}' not found.")

    # Read the SPARQL query that checks date completeness
    with open(query_file, "r") as file:
        query = file.read()

    # Run the query on the loaded RDF data
    results = store.query(query)

    # Counters to track how many observations have a date ("non_empty") and how many don't ("empty")
    non_empty_count = 0
    empty_count = 0

    print("\n=== Observations and Date Completeness ===")

    # Go through the query results and check each observation
    for row in results:
        observation = str(row["observation"]).strip("<>")  # Get the observation ID
        completeness_label = row["assess_date_completeness"].value  # Get the completeness label

        # If the observation has a date, mark it as "non_empty"
        if completeness_label == "non_empty":
            label = "non_empty"
            non_empty_count += 1  # Increase the count of non-empty observations
        else:  # Otherwise, mark it as "empty"
            label = "empty"
            empty_count += 1  # Increase the count of empty observations

        # Print details about the observation
        print(f"Observation: {observation}")
        print(f"Date Completeness Label: {label}")
        print("-----")

    # Print a summary of the results
    print("\n=== Summary ===")
    print(f"Total 'non_empty': {non_empty_count}")  # Total observations with a date
    print(f"Total 'empty': {empty_count}")  # Total observations without a date

# If this script is run directly, execute the function
if __name__ == "__main__":
    assess_date_completeness()
