from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# Define vocabularies
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
EX = Namespace("http://example.com/test/")

def create_datum_type_test_data():
    """
    Make RDF test data for checking type of coordinate datum.

    Create 5 observations:
    - 4 with different known datum types (AGD84, GDA94, GDA2020, EPSG:4326)
    - 1 with no datum (should be 'None')
    """

    g = Graph()

    # List of observations and their datum types
    datums = {
        "obs_agd84": "AGD84",
        "obs_gda94": "GDA94",
        "obs_gda2020": "GDA2020",
        "obs_wgs84": "EPSG:4326",
        "obs_none": None  # No datum for this one
    }

    for obs_id, datum in datums.items():
        obs = EX[obs_id]
        sample = EX[f"sample_{obs_id}"]
        proc = EX[f"proc_{obs_id}"]

        # Set observation structure
        g.add((obs, RDF.type, TERN.Observation))
        g.add((obs, SOSA.hasFeatureOfInterest, sample))
        g.add((sample, RDF.type, TERN.Sample))
        g.add((sample, SOSA.isResultOf, proc))

        # Add datum if it exists
        if datum:
            g.add((proc, GEO.hasGeometryDatum, Literal(datum, datatype=XSD.string)))

    return g.serialize(format="turtle")

# For manual check
if __name__ == "__main__":
    print(create_datum_type_test_data()[:1000])  # show first part of Turtle data
