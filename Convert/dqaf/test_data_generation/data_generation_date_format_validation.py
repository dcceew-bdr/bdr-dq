from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME

# Define the namespace for observations
OBS = Namespace("http://createme.org/observation/scientificName/")


def create_date_format_validation_test_data():
    """
    Generates RDF test_dq data to check if dates are formatted correctly.

    - "obs_valid_date" → Correctly formatted date (YYYY-MM-DD).
    - "obs_invalid_date_slash" → Uses slashes instead of hyphens (YYYY/MM/DD).
    - "obs_invalid_date_order" → Incorrect order (YYYY-DD-MM).
    - "obs_invalid_date_extra" → Contains extra characters (YYYY-MM-DDT12:00:00Z).
    - "obs_missing_date" → No date at all.
    """

    # Create an empty RDF graph
    g = Graph()

    # ===== Observation 1: Correct format (should be "valid") =====
    g.add((OBS["obs_valid_date"], RDF.type, OBS.Observation))
    g.add((OBS["obs_valid_date"], TIME.hasTime, OBS["time1"]))
    g.add((OBS["time1"], TIME.inXSDDateTimeStamp, Literal("2023-05-10T00:00:00", datatype=XSD.dateTime)))  # Correct

    # ===== Observation 2: Uses slashes instead of hyphens (should be "invalid") =====
    g.add((OBS["obs_invalid_date_slash"], RDF.type, OBS.Observation))
    g.add((OBS["obs_invalid_date_slash"], TIME.hasTime, OBS["time2"]))
    g.add((OBS["time2"], TIME.inXSDDateTimeStamp, Literal("2023/05/10", datatype=XSD.string)))  # Store as string

    # ===== Observation 3: Incorrect order (should be "invalid") =====
    g.add((OBS["obs_invalid_date_order"], RDF.type, OBS.Observation))
    g.add((OBS["obs_invalid_date_order"], TIME.hasTime, OBS["time3"]))
    g.add((OBS["time3"], TIME.inXSDDateTimeStamp, Literal("2023-31-12", datatype=XSD.string)))  # Store as string

    # ===== Observation 4: Extra characters (should be "invalid") =====
    g.add((OBS["obs_invalid_date_extra"], RDF.type, OBS.Observation))
    g.add((OBS["obs_invalid_date_extra"], TIME.hasTime, OBS["time4"]))
    g.add((OBS["time4"], TIME.inXSDDateTimeStamp,
           Literal("2023-05-10T12:00:00+00:00", datatype=XSD.dateTime)))  # Allowed in xsd:dateTime

    # ===== Observation 5: No date (should be ignored in validation) =====
    g.add((OBS["obs_missing_date"], RDF.type, OBS.Observation))  # No date assigned

    # Return the RDF data serialized in Turtle format
    return g.serialize(format="turtle")


# Run the function and print the generated test_dq data.
if __name__ == "__main__":
    turtle_data = create_date_format_validation_test_data()
    print(turtle_data)
