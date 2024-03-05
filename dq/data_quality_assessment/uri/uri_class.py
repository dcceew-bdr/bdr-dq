from rdflib import URIRef


class AssessmentTypes:
    OBSERVATION_DATE_RECENCY = URIRef("http://example.com/assess_observation_date_recency/")
    COORDINATE_PRECISION = URIRef("http://example.com/assess_coordinate_precision")
    POINT_IN_AUSTRALIA = URIRef("http://example.com/assess_point_in_australia")
    OBSERVATION_DATE_OUTLIERS = URIRef("http://example.com/assess_observation_date_outliers")
    POINT_IN_AUSTRALIA_STATE = URIRef("http://example.com/assess_point_in_australia_state")
    OBSERVATION_DATE_CHECK_FORMAT_VALIDATION = URIRef(
        "http://example.com/assess_observation_date_check_format_validation")
    OBSERVATION_LOCATION_OUTLIERS = URIRef("http://example.com/assess_observation_location_outliers")
    DATUM_NOT_EMPTY = URIRef("http://example.com/assess_datum_not_empty")


class BaseUris:
    OBSERVATION = "http://createme.org/observation/individualCount/"
    ATTRIBUTE = "http://createme.org/attribute/kingdom/"
    SCIENTIFIC_NAME = "http://createme.org/observation/scientificName/"
    PROVIDER = "http://createme.org/provider/"
    SAMPLE = "http://createme.org/sample/field/"

    @staticmethod
    def check_base_uri(uri, check_string):
        # Find the last occurrence of '/'
        last_slash_index = uri.rfind('/')
        # Extract the base URI
        base_uri = uri[:last_slash_index + 1]  # Include the slash in the base URI
        return base_uri == check_string
