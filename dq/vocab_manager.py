import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import SKOS, RDF


class VocabManager:
    def __init__(self):

        self.g = Graph()
        self.namespaces_and_labels = {
            "coordinate_precision": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_precision/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_precision/"),
                "prefix": "coordinate_precision",
                "labels": {
                    "Low": "Indicates low precision in coordinate values if either or both of the latitude or longitude of the location's coordinate has less than 2 decimal points.",
                    "Medium": "Indicates medium precision in coordinate values if either or both of the latitude or longitude of the location's coordinate has between 2 and 4 decimal points.",
                    "High": "Indicates high precision in coordinate values if latitude and longitude of the location's coordinate has more than 4 decimal points.",
                },
                "expanded_rule_definition": {
                    "Low": "If either the latitude or longitude values of the location coordinate in the 'geo:hasGeometry' field have less than 2 decimal places, label the record as 'Low'. This indicates a low level of precision in the coordinate values, suggesting a broad, general area rather than a specific location.",
                    "Medium": "If either the latitude or longitude values of the location coordinate in the 'geo:hasGeometry' field have between 2 and 4 decimal places, label the record as 'Medium'. This denotes a moderate level of precision in the coordinate values, pinpointing a more specific location but not with the highest degree of accuracy.",
                    "High": "If either the latitude or longitude values of the location coordinate in the 'geo:hasGeometry' field have more than 4 decimal places, label the record as 'High'. This signifies a high level of precision in the coordinate values, indicating a very specific location with detailed geographical accuracy.",
                },
            },

            "coordinate_completeness": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_completeness/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_completeness/"),
                "prefix": "coordinate_completeness",
                "labels": {
                    "empty": "This label is used to mark records where no geographic coordinate data is provided, indicating an absence of specific latitude and longitude information in the geometry of the feature.",
                    "non_empty": "This label is applied to records that contain valid geographic coordinate data, signifying the presence of specific latitude and longitude information in the feature's geometry.",
                },
                "expanded_rule_definition": {
                    "empty": "If the 'geo:hasGeometry' field does not exist or contains no data, label the record as 'empty'. This indicates an absence of geographic coordinate data, highlighting that no specific latitude and longitude information is provided.",
                    "non_empty": "If the 'geo:hasGeometry' field exists and contains data, label the record as 'non_empty'. This signifies the presence of specific latitude and longitude information, indicating that geographic coordinate data is provided.",
                },
            },

            "coordinate_unusual": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "expanded_rule_definition": {
                    "usual": "If the latitude and longitude values within the 'geo:hasGeometry' field do not exhibit any repeating patterns in their decimal parts, label the record as 'usual'. This suggests that the geographic coordinates data appears normal, without any detectable anomalies or fabrication indicating potential inaccuracies.",
                    "unusual": "If either the latitude or longitude values (or both) within the 'geo:hasGeometry' field show repeating patterns in their decimal parts, label the record as 'unusual'. This implies that the geographic coordinates data may be inaccurate, fabricated, or exhibit atypical characteristics that deviate from normal precision or representation.",
                },
                "namespace": Namespace("http://example.com/vocab/coordinate_unusual/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_unusual/"),
                "prefix": "coordinate_unusual",
                "labels": {
                    "usual": "This label is assigned to records where latitude and longitude values do not exhibit any repeating patterns in their decimal parts, indicating that the geographic coordinate data is considered normal and without abnormalities or fabrication.",
                    "unusual": "This label is applied to records where either latitude or longitude (or both) show repeating patterns in their decimal parts, suggesting that the geographic coordinate data may be inaccurate, fabricated, or otherwise atypical.",
                },
            },

            "coordinate_in_australia_state": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_in_australia_state/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_in_australia_state/"),
                "prefix": "coordinate_in_australia_state",
                "labels": {
                    "New_South_Wales": "Indicates that the coordinate is in New South Wales, a state on the east coast of Australia.",
                    "Victoria": "Indicates that the coordinate is in Victoria, a state in southeast Australia.",
                    "Queensland": "Indicates that the coordinate is in Queensland, a state in northeast Australia.",
                    "Western_Australia": "Indicates that the coordinate is in Western Australia, a state occupying the entire western third of Australia.",
                    "South_Australia": "Indicates that the coordinate is in South Australia, a state in the southern central part of Australia.",
                    "Tasmania": "Indicates that the coordinate is in Tasmania, an island state off the southern coast of Australia.",
                    "Northern_Territory": "Indicates that the coordinate is in the Northern Territory, a federal Australian territory in the center and central northern regions.",
                    "Australian_Capital_Territory": "Indicates that the coordinate is in the Australian Capital Territory, Australia's federal district, located in the southeast of the country.",
                    "Outside_Australia": "Indicates that the coordinate is outside the geographical bounds of Australia.",
                },
                "expanded_rule_definition": {
                    "New_South_Wales": "If the geographic coordinate falls within the boundaries of New South Wales, label the record as 'New_South_Wales'.",
                    "Victoria": "If the geographic coordinate is located within Victoria's boundaries, label the record as 'Victoria'.",
                    "Queensland": "If the geographic coordinate lies within Queensland, label the record as 'Queensland'. ",
                    "Western_Australia": "If the geographic coordinate is situated within Western Australia, label the record as 'Western_Australia'.",
                    "South_Australia": "If the geographic coordinate is found within South Australia, label the record as 'South_Australia'. ",
                    "Tasmania": "If the geographic coordinate is located within Tasmania, label the record as 'Tasmania'. ",
                    "Northern_Territory": "If the geographic coordinate falls within the Northern Territory, label the record as 'Northern_Territory'. ",
                    "Australian_Capital_Territory": "If the geographic coordinate is within the Australian Capital Territory, label the record as 'Australian_Capital_Territory'. ",
                    "Outside_Australia": "If the geographic coordinate does not fall within the geographical bounds of any Australian states or territories, label the record as 'Outside_Australia'.",
                },
            },

            "coordinate_outlier_irq": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_outlier_irq/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_outlier_irq/"),
                "prefix": "coordinate_outlier_irq",
                "labels": {
                    "outlier_coordinate": "This label indicates that the observation coordinate significantly deviates from the typical range, suggesting it may be an anomaly. (Based on IRQ Method)",
                    "normal_coordinate": "This label indicates that the observation coordinate falls within the typical range, suggesting it is not an anomaly. (Based on IRQ Method)",
                },
                "expanded_rule_definition": {
                    "outlier_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field significantly deviates from the typical range based on the Interquartile Range (IRQ) method—meaning the point's coordinate values fall outside the bounds established by the IRQ calculations (e.g., below Q1 - 1.5IQR or above Q3 + 1.5IQR for either latitude or longitude)—label the record as 'outlier_point'. This indicates the observation point is considered an anomaly, significantly deviating from the common geographic location range. ",
                    "normal_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field falls within the typical range, as determined by the Interquartile Range (IRQ) method—meaning the point's coordinate values are within the bounds set by Q1 - 1.5IQR and Q3 + 1.5IQR for both latitude and longitude—label the record as 'normal_point'. This suggests the observation point does not significantly deviate from the expected geographic location range, indicating it is not considered an anomaly.",
                },
            },
            "coordinate_outlier_isolation_forest": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_outlier_isolation_forest/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_outlier_isolation_forest/"),
                "prefix": "coordinate_outlier_isolation_forest",
                "labels": {
                    "outlier_coordinate": "This label indicates that the observation coordinate significantly deviates from the typical range, suggesting it may be an anomaly. (Based on Isolation Forest Method)",
                    "normal_coordinate": "This label indicates that the observation coordinate falls within the typical range, suggesting it is not an anomaly. (Based on Isolation Forest Method)",
                },
                "expanded_rule_definition": {
                    "outlier_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field is identified as an outlier by the Isolation Forest algorithm—meaning it falls outside the typical range of coordinates—label the record as 'outlier_point'. This indicates the observation point is considered an anomaly, significantly deviating from the common geographic location range.",
                    "normal_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field is not identified as an outlier by the Isolation Forest algorithm—meaning it falls within the typical range of coordinates—label the record as 'normal_point'. This suggests the observation point does not significantly deviate from the expected geographic location range, indicating it is not considered an anomaly.",
                },
            }
            ,
            "coordinate_outlier_robust_covariance": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_outlier_robust_covariance/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_outlier_robust_covariance/"),
                "prefix": "coordinate_outlier_robust_covariance",
                "labels": {
                    "outlier_coordinate": "This label indicates that the observation coordinate significantly deviates from the typical range, suggesting it may be an anomaly. (Based on Robust Covariance Method)",
                    "normal_coordinate": "This label indicates that the observation coordinate falls within the typical range, suggesting it is not an anomaly. (Based on Robust Covariance Method)",
                },
                "expanded_rule_definition": {
                    "outlier_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field is identified as an outlier by the Robust Covariance algorithm—meaning it falls outside the typical range of coordinates—label the record as 'outlier_point'. This indicates the observation point is considered an anomaly, significantly deviating from the common geographic location range.",
                    "normal_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field is not identified as an outlier by the Robust Covariance algorithm—meaning it falls within the typical range of coordinates—label the record as 'normal_point'. This suggests the observation point does not significantly deviate from the expected geographic location range, indicating it is not considered an anomaly.",
                },
            }

            ,

            "coordinate_outlier_zscore": {
                "category": "coordinate",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/coordinate_outlier_zscore/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_outlier_zscore/"),
                "prefix": "coordinate_outlier_zscore",
                "labels": {
                    "outlier_coordinate": "This label indicates that the observation coordinate significantly deviates from the typical range, suggesting it may be an anomaly. (Based on Z-Score Method)",
                    "normal_coordinate": "This label indicates that the observation coordinate falls within the typical range, suggesting it is not an anomaly. (Based on Z-Score Method)",
                },
                "expanded_rule_definition": {
                    "outlier_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field significantly deviates from the mean, based on the Z-Score method—meaning the coordinates Z-Score is beyond a predefined threshold (typically, a Z-Score greater than 3 or less than -3 for either latitude or longitude)—label the record as 'outlier_point'. This suggests the observation point is an anomaly, significantly deviating from the standard range of geographic locations. ",
                    "normal_coordinate": "If the geographic coordinate data (latitude and/or longitude) from the 'geo:hasGeometry' field has a Z-Score within a normal range (typically, a Z-Score between -3 and 3 for both latitude and longitude), based on the Z-Score method, label the record as 'normal_point'. This indicates the observation coordinates falls within the expected range of geographic locations, suggesting it is not considered an anomaly.",
                },
            },

            "date_recency": {
                "category": "date",
                "input_field_(RDF)": "sosa:phenomenonTime",
                "namespace": Namespace("http://example.com/vocab/date_recency/"),
                "assess_namespace": URIRef("http://example.com/assess/date_recency/"),
                "prefix": "date_recency",
                "labels": {
                    "recent_20_years": "This label indicates that the observation date is within the last 20 years, making it more relevant to current contexts and studies.",
                    "outdated_20_years": "This label indicates that the observation date is more than 20 years ago, before 20 years, and may not reflect the current state or conditions.",
                },
                "expanded_rule_definition": {
                    "recent_20_years": "If the 'sosa:phenomenonTime' field contains a date that falls within the last 20 years from the current date, label the record as 'recent'. This label suggests the observation is relevant to current contexts and studies due to its recency. ",
                    "outdated_20_years": "If the 'sosa:phenomenonTime' field contains a date that is more than 20 years ago from the current date, label the record as 'outdated'. This indicates the observation may not reflect current conditions, deeming it potentially less relevant for recent applications or analyses.",
                },
            },

            "duplicate": {
                "category": "data_quality",
                "input_field_(RDF)": "various_fields",  # Since multiple predicates can be used
                "namespace": Namespace("http://example.com/vocab/duplicate/"),
                "assess_namespace": URIRef("http://example.com/assess/duplicate/"),
                "prefix": "duplicate_value_combination",
                "labels": {
                    "inferred_duplicate": "Indicates that the record has a combination of values across multiple fields that are identical to other records.",
                    "inferred_nonduplicate": "Indicates that the record has a unique combination of values across multiple fields that is not shared by other records.",
                },
                "expanded_rule_definition": {
                    "inferred_duplicate": "If the record has a combination of values across the specified fields that is identical to other records in the dataset, label it as 'duplicate_combination'. This implies redundancy in data values for multiple records.",
                    "inferred_nonduplicate": "If the record has a unique combination of values across the specified fields, label it as 'unique_combination'. This means that no other records share this exact combination.",
                },
            },
            "geo_spatial_accuracy_precision": {
                "category": "geo",
                "input_field_(RDF)": "geo:hasMetricSpatialAccuracy",
                "namespace": Namespace("http://example.com/vocab/geo_spatial_accuracy_precision/"),
                "assess_namespace": URIRef("http://example.com/assess/geo_spatial_accuracy_precision/"),
                "prefix": "geo_spatial_accuracy_precision",
                "labels": {
                    "low_precision": "Indicates that the spatial accuracy is low, either because the value of coordinateUncertaintyInMeters is empty or exceeds 10,000 meters.",
                    "high_precision": "Indicates that the spatial accuracy is high, meaning the value of coordinateUncertaintyInMeters is less than or equal to 10,000 meters.",
                },
                "expanded_rule_definition": {
                    "low_precision": "If the 'coordinateUncertaintyInMeters' field is empty or its value exceeds 10,000, label the record as 'low_precision'. This indicates that the precision of the spatial accuracy is insufficient.",
                    "high_precision": "If the 'coordinateUncertaintyInMeters' field contains a value of 10,000 or less, label the record as 'high_precision'. This indicates that the precision of the spatial accuracy is adequate.",
                },
            },

            "date_format_validation": {
                "category": "date",
                "input_field_(RDF)": "sosa:phenomenonTime",
                "namespace": Namespace("http://example.com/vocab/date_format_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/date_format_validation/"),
                "prefix": "date_format_validation",
                "labels": {
                    "valid": "Indicates that the date format is valid and recognized.",
                    "invalid": "Indicates that the date format is invalid or unrecognized.",
                },
                "expanded_rule_definition": {
                    "valid": "If the date format in the 'sosa:phenomenonTime' field adheres to recognized and accepted standards, label the record as 'valid'. This indicates that the date is structured in a manner that is universally understood and correctly interpretable by systems and users alike. ",
                    "invalid": "If the date format in the 'sosa:phenomenonTime' field does not follow recognized and accepted standards or is structured in a way that is not correctly interpretable (e.g., mixing up day and month in a non-standard format), label the record as 'invalid'. This suggests that the date may be prone to misinterpretation or errors in processing due to its unconventional format.",
                },
            },

            "date_completeness": {
                "category": "date",
                "input_field_(RDF)": "sosa:phenomenonTime",
                "namespace": Namespace("http://example.com/vocab/date_completeness/"),
                "assess_namespace": URIRef("http://example.com/assess/date_completeness/"),
                "prefix": "date_completeness",
                "labels": {
                    "empty": "Indicates that the date is empty.",
                    "non_empty": "Indicates that the date is not empty.",
                },
                "expanded_rule_definition": {
                    "empty": "If the 'sosa:phenomenonTime' field does not exist or contains no data for a given record, label the record as 'empty'. This indicates that there is no date information provided, signifying an absence of temporal data for the observation. Non_Empty: If the 'sosa:phenomenonTime' field exists and contains data for a given record, label the record as 'non_empty'. This signifies that date information is present, indicating the availability of temporal data for the observation.",
                    "non_empty": "If the 'sosa:phenomenonTime' field does not exist or contains no data for a given record, label the record as 'empty'. This indicates that there is no date information provided, signifying an absence of temporal data for the observation. Non_Empty: If the 'sosa:phenomenonTime' field exists and contains data for a given record, label the record as 'non_empty'. This signifies that date information is present, indicating the availability of temporal data for the observation.",
                },
            },

            "date_outlier_kmeans": {
                "category": "date",
                "input_field_(RDF)": "sosa:phenomenonTime",
                "namespace": Namespace("http://example.com/vocab/date_outlier_kmeans/"),
                "assess_namespace": URIRef("http://example.com/assess/date_outlier_kmeans/"),
                "prefix": "date_outlier_kmeans",
                "labels": {
                    "outlier_date": "This label is used to tag dates that are determined to be significantly different from the majority, based on the KMeans clustering algorithm. Such dates fall into the smallest cluster or are far from the centroids of their clusters, indicating they deviate notably from typical date values.",
                    "normal_date": "This label is applied to dates that are considered to be within the expected range, based on the KMeans clustering results. These dates fall into larger clusters and are close to the centroids, indicating they align with the common patterns observed in the dataset.",
                },
                "expanded_rule_definition": {
                    "outlier_date": "If the date from the 'sosa:phenomenonTime' field is significantly different from the majority, as determined by falling into the smallest cluster or being far from the centroids of their clusters when analyzed by the KMeans clustering algorithm, label the record as 'outlier_date'. This label indicates the date deviates notably from typical date values, suggesting it might be an outlier. ",
                    "normal_date": "If the date from the 'sosa:phenomenonTime' field falls into larger clusters and is close to the centroids, according to the KMeans clustering results, label the record as 'normal_date'. This suggests the date aligns with common patterns observed in the dataset, indicating it is within the expected range of dates and considered normal.",
                },
            },

            "date_outlier_irq": {
                "category": "date",
                "input_field_(RDF)": "sosa:phenomenonTime",
                "namespace": Namespace("http://example.com/vocab/date_outlier_irq/"),
                "assess_namespace": URIRef("http://example.com/assess/date_outlier_irq/"),
                "prefix": "date_outlier_irq",
                "labels": {
                    "outlier_date": "This label indicates that the observation date significantly deviates from the typical range, suggesting it may be an anomaly. (Based on IRQ Method)",
                    "normal_date": "This label indicates that the observation date falls within the typical range, suggesting it is not an anomaly. (Based on IRQ Method)",
                },
                "expanded_rule_definition": {
                    "outlier_date": "If the date from the 'sosa:phenomenonTime' field significantly deviates from the typical range, based on the Interquartile Range (IRQ) method—meaning it falls outside the bounds established by the IRQ calculations (e.g., below Q1 - 1.5IQR or above Q3 + 1.5IQR)—label the record as 'outlier_date'. This label indicates that the date is considered an anomaly, deviating notably from the expected date range.",
                    "normal_date": "If the date from the 'sosa:phenomenonTime' field falls within the typical range, as determined by the Interquartile Range (IRQ) method—meaning it is within the bounds set by Q1 - 1.5IQR and Q3 + 1.5IQR—label the record as 'normal_date'. This suggests the date does not significantly deviate from what is typically observed, indicating it is not considered an anomaly.",
                },
            },

            "scientific_name_completeness": {
                "category": "scientific_name",
                "input_field_(RDF)": "tern:FeatureOfInterest",
                "namespace": Namespace("http://example.com/vocab/scientific_name_completeness/"),
                "assess_namespace": URIRef("http://example.com/assess/scientific_name_completeness/"),
                "prefix": "scientific_name_completeness",
                "labels": {
                    "empty_name": "This label is used to mark records where the scientific name field is missing or contains no data, indicating a lack of specified scientific identification for the observation or entity.",
                    "non_empty_name": "This label is applied to records that have a valid scientific name provided, indicating the presence of specified scientific identification for the observation or entity.",
                },
                "expanded_rule_definition": {
                    "empty_name": "If the 'tern:FeatureOfInterest' field does not exist or contains no data for a given record, label the record as 'empty_name'. This indicates the absence of a scientific name, signifying that specific scientific identification for the observation or entity is missing. ",
                    "non_empty_name": "If the 'tern:FeatureOfInterest' field exists and contains data for a given record, label the record as 'non_empty_name'. This signifies the presence of a scientific name, indicating that specific scientific identification for the observation or entity has been provided.",
                },
            },

            "scientific_name_validation": {
                "category": "scientific_name",
                "input_field_(RDF)": "tern:FeatureOfInterest",
                "namespace": Namespace("http://example.com/vocab/scientific_name_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/scientific_name_validation/"),
                "prefix": "scientific_name_validation",
                "labels": {
                    "valid_name": "This label is applied to records where the scientific name has been verified as correct and adheres to accepted naming conventions or validation criteria, indicating the scientific name is legitimate and accurately represents the entity.",
                    "invalid_name": "This label is used for records with scientific names that do not meet the established validation criteria, suggesting the name might be incorrect, misspelled, or not conforming to accepted scientific naming conventions.",
                },
                "expanded_rule_definition": {
                    "valid_name": "If the scientific name in the 'tern:FeatureOfInterest' field has been verified against accepted naming conventions or validation criteria and is found to be correct, label the record as 'valid_name'. This indicates that the scientific name is legitimate and accurately represents the observed entity, adhering to the recognized standards for scientific nomenclature. ",
                    "invalid_name": "If the scientific name in the 'tern:FeatureOfInterest' field does not meet established validation criteria—whether due to being incorrect, misspelled, or not conforming to accepted scientific naming conventions—label the record as 'invalid_name'. This suggests that the name may not be legitimate or accurately represent the entity as per the recognized standards for scientific nomenclature.",
                },
            },

            "datum_completeness": {
                "category": "datum",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/datum_completeness/"),
                "assess_namespace": URIRef("http://example.com/assess/datum_completeness/"),
                "prefix": "datum_completeness",
                "labels": {
                    "empty": "Indicates that the datum link reference is empty.",
                    "not_empty": "Indicates that the datum link reference is not empty.",
                },
                "expanded_rule_definition": {
                    "empty": "If the 'geo:hasGeometry' field either does not exist or contains no link reference data for a given record, label the record as 'empty'. This label indicates the absence of a datum link reference, signifying that no specific geographic datum information is provided for the geographic coordinate data. ",
                    "not_empty": "If the 'geo:hasGeometry' field exists and contains link reference data for a given record, label the record as 'not_empty'. This label signifies the presence of a datum link reference, indicating that specific geographic datum information is provided for the geographic coordinate data.",
                },
            },

            "datum_validation": {
                "category": "datum",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/datum_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/datum_validation/"),
                "prefix": "datum_validation",
                "labels": {
                    "valid": "Indicates that the datum link reference is valid and recognized.",
                    "invalid": "Indicates that the datum link reference is invalid or unrecognized.",
                },
                "expanded_rule_definition": {
                    "valid": "If the datum link reference in the 'geo:hasGeometry' field is recognized and conforms to known and accepted geographic datum standards, label the record as 'valid'. This indicates that the datum link reference is appropriate and can be reliably used for geographic coordinate data interpretation.",
                    "invalid": "If the datum link reference in the 'geo:hasGeometry' field is not recognized or does not conform to known and accepted geographic datum standards, label the record as 'invalid'. This indicates that the datum link reference may be incorrect, fabricated, or not suitable for accurate geographic coordinate data interpretation.",
                },
            },

            "datum_type": {
                "category": "datum",
                "input_field_(RDF)": "geo:hasGeometry",
                "namespace": Namespace("http://example.com/vocab/datum_type/"),
                "assess_namespace": URIRef("http://example.com/assess/datum_type/"),
                "prefix": "datum_type",
                "labels": {
                    "AGD84": "Indicates that the datum is in the Australian Geodetic Datum 1984 type.",
                    "GDA2020": "Indicates that the datum is in the Geocentric Datum of Australia 2020 type.",
                    "GDA94": "Indicates that the datum is in the Geocentric Datum of Australia 1994 type.",
                    "WGS84": "Indicates that the datum is in the World Geodetic System 1984 type.",
                    "None": "Indicates that the datum is not in the AGD84, GDA2020, GDA94, or WGS84 types."
                },
                "expanded_rule_definition": {
                    "AGD84": "If the datum link reference within the 'geo:hasGeometry' field specifies the Australian Geodetic Datum 1984 (AGD84), label the record as 'AGD84'. This classification indicates that the geographic data is referenced according to the AGD84 standard. ",
                    "GDA2020": "If the datum link reference in the 'geo:hasGeometry' field is identified as the Geocentric Datum of Australia 2020 (GDA2020), label the record as 'GDA2020'. This shows that the geographic data adheres to the GDA2020 standard, a more recent datum for Australia. ",
                    "GDA94": "If the datum link reference in the 'geo:hasGeometry' field corresponds to the Geocentric Datum of Australia 1994 (GDA94), label the record as 'GDA94'. This indicates the use of the GDA94 standard, preceding GDA2020 for Australian geographic data.",
                    "WGS84": "If the datum link reference in the 'geo:hasGeometry' field is recognized as the World Geodetic System 1984 (WGS84), label the record as 'WGS84'. This classification signifies that the geographic data is based on the globally used WGS84 standard.",
                    "None": "If the datum link reference in the 'geo:hasGeometry' field does not correspond to any of the specified types (AGD84, GDA2020, GDA94, WGS84), label the record as 'None'. This label indicates that the datum used does not match the predefined types, suggesting either a different standard is in use or the datum type is unspecified."
                },
            },
        }

    def init_assessment(self, namespace_key):
        if namespace_key in self.namespaces_and_labels:
            total_assessments = 0

            result_counts = {}
            for label in self.namespaces_and_labels[namespace_key]["labels"]:
                result_counts[label] = 0

            return self.namespaces_and_labels[namespace_key]["namespace"], self.namespaces_and_labels[namespace_key][
                "assess_namespace"], result_counts, total_assessments
        else:
            raise KeyError(f"Namespace '{namespace_key}' not found in the namespaces_and_labels dictionary.")

    def get_all_labels(self):
        all_labels_with_prefix = list()
        for namespace_key, namespace_info in self.namespaces_and_labels.items():
            prefix = namespace_info['prefix']
            labels = namespace_info['labels']
            for label in labels.keys():
                all_labels_with_prefix.append(f"{prefix}:{label}")
        return all_labels_with_prefix

    def create_excel_template(self, output_filename):
        rows = []
        dq_assertions = []

        for key, value in self.namespaces_and_labels.items():
            prefix = value["prefix"]
            for label, label_description in value["labels"].items():
                expanded_rule_definition = value.get("expanded_rule_definition", {}).get(label, "")

                row = {
                    'Data Quality Assertion': f"{prefix}:{label}",
                    'Category': value["category"],
                    'Input field (RDF)': value["input_field_(RDF)"],
                    'Label': label,
                    'Simple Rule Definition': label_description,
                    'Expanded Rule Definition': expanded_rule_definition,
                }
                rows.append(row)

                dq_assertion_row = {
                    'Data Quality Assertion': f"{prefix}:{label}",
                    'New Use Case Name': ''
                }
                dq_assertions.append(dq_assertion_row)

        df = pd.DataFrame(rows)
        df_dq_assertions = pd.DataFrame(dq_assertions)

        with pd.ExcelWriter(output_filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_dq_assertions.to_excel(writer, sheet_name='Data quality assertion', index=False)
            df.to_excel(writer, sheet_name='Definition of assertions', index=False)

    def create_output_definition_file(self, output_filename):
        self.bind_custom_namespaces()
        self.add_label_definitions()
        self.g.serialize(destination=output_filename, format="turtle")
        print(f"Graph has been serialized to {output_filename}.")

    def bind_custom_namespaces(self, graph=None):
        if graph is None:
            graph = self.g

        graph.bind("skos", SKOS)
        for namespace_key, namespace_info in self.namespaces_and_labels.items():
            graph.bind(namespace_info["prefix"], namespace_info["namespace"])

    def add_label_definitions(self):
        for namespace_key, namespace_info in self.namespaces_and_labels.items():
            namespace = namespace_info["namespace"]
            labels_info = namespace_info["labels"]
            for label, definition in labels_info.items():
                label_uri = namespace[label]
                self.g.add((label_uri, RDF.type, SKOS.Concept))
                self.g.add((label_uri, SKOS.prefLabel, Literal(label.capitalize())))
                self.g.add((label_uri, SKOS.definition, Literal(definition)))
