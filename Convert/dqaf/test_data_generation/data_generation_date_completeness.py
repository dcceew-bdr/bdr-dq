from rdflib import Graph, Namespace, Literal  # Import libraries to handle RDF data
from rdflib.namespace import RDF, XSD, TIME  # Import common RDF namespaces

# Define a namespace (like a category for data) for observations
OBS = Namespace("http://createme.org/observation/scientificName/")

def create_date_completeness_test_data():
    """
    This function creates test_dq data to check if observations have a date.

    - "obs_with_date" → Has a valid date (should be labeled "non_empty").
    - "obs_no_date" → No date at all (should be labeled "empty").
    - "obs_missing_date" → Has a time reference but no actual date (should be "empty").
    """

    # Create an empty RDF graph (like a database to store the test_dq data)
    g = Graph()

    # ===== Observation 1: Has a valid date (should be labeled "non_empty") =====
    g.add((OBS["obs_with_date"], RDF.type, OBS.Observation))  # Define as an observation
    g.add((OBS["obs_with_date"], TIME.hasTime, OBS["time1"]))  # Link observation to a time record
    g.add((OBS["time1"], TIME.inXSDgYear, Literal("2023", datatype=XSD.gYear)))  # Assign a valid date (2023)

    # ===== Observation 2: No date at all (should be labeled "empty") =====
    g.add((OBS["obs_no_date"], RDF.type, OBS.Observation))  # Define as an observation but no date is provided

    # ===== Observation 3: Has a time reference but missing actual date (should be labeled "empty") =====
    g.add((OBS["obs_missing_date"], RDF.type, OBS.Observation))  # Define as an observation
    g.add((OBS["obs_missing_date"], TIME.hasTime, OBS["time2"]))  # Time reference exists
    # ⚠ No `time:inXSDgYear` property for time2, meaning the date is missing

    # Return the RDF data serialized in Turtle format instead of writing to a file
    return g.serialize(format="turtle")

# Run the function and print the generated test_dq data.
if __name__ == "__main__":
    turtle_data = create_date_completeness_test_data()
    print(turtle_data)
