from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define short names for common URIs
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
EX = Namespace("http://example.com/test/")

def create_scientific_name_validation_test_data():
    """
    Make RDF test data for checking scientific name validation.

    It has 2 cases:
    - One with a real name (should be valid)
    - One with fake name (should be invalid)

    But current rule returns both as "valid_name" because it is a placeholder only.
    """

    g = Graph()

    # === Observation 1: Looks like a valid name
    obs1 = EX["obs_valid"]
    feature1 = EX["feature1"]
    g.add((obs1, RDF.type, TERN.Observation))
    g.add((obs1, SOSA.hasFeatureOfInterest, feature1))
    g.add((feature1, DWC.scientificName, Literal("Acacia dealbata", datatype=XSD.string)))

    # === Observation 2: Looks like a fake name
    obs2 = EX["obs_invalid"]
    feature2 = EX["feature2"]
    g.add((obs2, RDF.type, TERN.Observation))
    g.add((obs2, SOSA.hasFeatureOfInterest, feature2))
    g.add((feature2, DWC.scientificName, Literal("Invalidus nonexistus", datatype=XSD.string)))

    return g.serialize(format="turtle")

# Show result if run directly
if __name__ == "__main__":
    print(create_scientific_name_validation_test_data()[:1000])
