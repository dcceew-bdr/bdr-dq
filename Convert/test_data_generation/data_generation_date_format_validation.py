from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD, TIME, RDFS

# Use these to define meaning of triples
SOSAN = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
EX = Namespace("http://example.com/obs/")  # Base for example resources

def create_date_format_validation_test_data():
    """
    This function makes test data to check date format.

    We make 3 test cases:
    - One has good date format (YYYY-MM-DD)
    - One has bad date format (no dashes)
    - One has good date but should not be tested (comment is different)
    """

    g = Graph()

    # === Test 1: Valid format ===
    # Has date like 2023-08-25
    # Comment includes needed phrase, so should be checked
    g.add((EX["obs_valid"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_valid"], SOSAN.phenomenonTime, EX["time1"]))
    g.add((EX["time1"], TIME.inXSDDateTimeStamp, Literal("2023-08-25T12:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_valid"], RDFS.comment, Literal("NSL name match Observation - valid date format")))

    # === Test 2: Invalid format ===
    # Has date like 20230825 (wrong format)
    # Comment includes needed phrase, so should be checked
    g.add((EX["obs_invalid"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_invalid"], SOSAN.phenomenonTime, EX["time2"]))
    g.add((EX["time2"], TIME.inXSDDateTimeStamp, Literal("20230825T12:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_invalid"], RDFS.comment, Literal("NSL name match Observation - invalid date format")))

    # === Test 3: Should be ignored ===
    # Date is OK, but comment does not match, so rule should skip it
    g.add((EX["obs_ignore"], RDF.type, SOSAN.Observation))
    g.add((EX["obs_ignore"], SOSAN.phenomenonTime, EX["time3"]))
    g.add((EX["time3"], TIME.inXSDDateTimeStamp, Literal("2022-01-01T00:00:00", datatype=XSD.dateTimeStamp)))
    g.add((EX["obs_ignore"], RDFS.comment, Literal("Other type of observation")))

    return g.serialize(format="turtle")

# Show the Turtle output if run directly
if __name__ == "__main__":
    print(create_date_format_validation_test_data())
