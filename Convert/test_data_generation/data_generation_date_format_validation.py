from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME, RDFS

# ===============================
# Define the namespace for terms
# ===============================
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
EX = Namespace("http://example.com/obs/")  # Custom example base

def create_date_format_validation_test_data():
    """
    This function creates RDF test data for checking date format validation.

    It includes:
    - One observation with a valid date format (YYYY-MM-DD)
    - One observation with an invalid format (e.g., missing dash or wrong pattern)
    - One observation with a valid date, but not matching the filter (should be ignored)
    """

    g = Graph()

    # ====================================
    # Observation 1: Valid date format
    # Format: 2023-08-25T12:00:00 → valid
    # Should be included (matches comment filter)
    # ====================================
    g.add((EX["obs_valid"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_valid"], SOSAN.phenomenonTime, EX["time1"]))
    g.add((EX["time1"], TIME.inXSDDateTimeStamp, Literal("2023-08-25T12:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_valid"], RDFS.comment, Literal("NSL name match Observation - valid date format")))

    # ====================================
    # Observation 2: Invalid date format
    # Format: 20230825T12:00:00 → invalid
    # Should be included (matches comment filter)
    # ====================================
    g.add((EX["obs_invalid"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_invalid"], SOSAN.phenomenonTime, EX["time2"]))
    g.add((EX["time2"], TIME.inXSDDateTimeStamp, Literal("20230825T12:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_invalid"], RDFS.comment, Literal("NSL name match Observation - invalid date format")))

    # ====================================
    # Observation 3: Valid date but comment does not match filter
    # Should be ignored
    # ====================================
    g.add((EX["obs_ignore"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_ignore"], SOSAN.phenomenonTime, EX["time3"]))
    g.add((EX["time3"], TIME.inXSDDateTimeStamp, Literal("2022-01-01T00:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_ignore"], RDFS.comment, Literal("Other type of observation")))

    return g.serialize(format="turtle")

# For manual test
if __name__ == "__main__":
    print(create_date_format_validation_test_data())
