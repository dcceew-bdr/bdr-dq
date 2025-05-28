from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Set short names for URIs
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
EX = Namespace("http://example.com/test/")

def create_scientific_name_completeness_test_data():
    """
    This function creates test RDF data for scientific name completeness check.

    It has 2 examples:
    - One observation has a name → should return "non_empty_name"
    - One observation without name → should return "empty_name"
    """

    g = Graph()

    # === Observation 1: With name (should be non_empty_name)
    obs1 = EX["obs_with_name"]
    feature1 = EX["feature1"]
    g.add((obs1, RDF.type, TERN.Observation))
    g.add((obs1, SOSA.hasFeatureOfInterest, feature1))
    g.add((feature1, DWC.scientificName, Literal("Eucalyptus globulus", datatype=XSD.string)))

    # === Observation 2: No name (should be empty_name)
    obs2 = EX["obs_no_name"]
    feature2 = EX["feature2"]
    g.add((obs2, RDF.type, TERN.Observation))
    g.add((obs2, SOSA.hasFeatureOfInterest, feature2))
    # No scientificName for feature2

    return g.serialize(format="turtle")

# Show test data if run directly
if __name__ == "__main__":
    print(create_scientific_name_completeness_test_data()[:1000])
