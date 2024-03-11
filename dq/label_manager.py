from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import SKOS, RDF
import pandas as pd


class LabelManager:
    def __init__(self):

        self.g = Graph()
        self.namespaces_and_labels = {
            "date_recency": {
                "namespace": Namespace("http://example.com/vocab/date_recency/"),
                "assess_namespace": URIRef("http://example.com/assess/date_recency/"),
                "prefix": "date_recency",
                "labels": {
                    "recent": "This label indicates that the observation date is within the last 20 years, making it more relevant to current contexts and studies.",
                    "outdated": "This label indicates that the observation date is more than 20 years ago, before 20 years, and may not reflect the current state or conditions.",
                },
            },
            "point_is_empty": {
                "namespace": Namespace("http://example.com/vocab/point_is_empty/"),
                "assess_namespace": URIRef("http://example.com/assess/point_is_empty/"),
                "prefix": "point_is_empty",
                "labels": {
                    "empty": "This label is used to mark records where no geographic point data is provided, indicating an absence of specific latitude and longitude information in the geometry of the feature.",
                    "non_empty": "This label is applied to records that contain valid geographic point data, signifying the presence of specific latitude and longitude information in the feature's geometry.",
                }
            },
            "point_unusual": {
                "namespace": Namespace("http://example.com/vocab/point_unusual/"),
                "assess_namespace": URIRef("http://example.com/assess/point_unusual/"),
                "prefix": "point_unusual",
                "labels": {
                    "usual": "This label is assigned to records where latitude and longitude values do not exhibit any repeating patterns in their decimal parts, indicating that the geographic point data is considered normal and without abnormalities.",
                    "unusual": "This label is applied to records where either latitude or longitude (or both) show repeating patterns in their decimal parts, suggesting that the geographic point data may be inaccurate, fabricated, or otherwise atypical.",
                }
            },
            "scientific_name_is_empty": {
                "namespace": Namespace("http://example.com/vocab/scientific_name_is_empty/"),
                "assess_namespace": URIRef("http://example.com/assess/scientific_name_is_empty/"),
                "prefix": "scientific_name_is_empty",
                "labels": {
                    "empty_name": "This label is used to mark records where the scientific name field is missing or contains no data, indicating a lack of specified scientific identification for the observation or entity.",
                    "non_empty_name": "This label is applied to records that have a valid scientific name provided, indicating the presence of specified scientific identification for the observation or entity.",
                }
            },
            "scientific_name_validation": {
                "namespace": Namespace("http://example.com/vocab/scientific_name_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/scientific_name_validation/"),
                "prefix": "scientific_name_validation",
                "labels": {
                    "valid_name": "This label is applied to records where the scientific name has been verified as correct and adheres to accepted naming conventions or validation criteria, indicating the scientific name is legitimate and accurately represents the entity.",
                    "invalid_name": "This label is used for records with scientific names that do not meet the established validation criteria, suggesting the name might be incorrect, misspelled, or not conforming to accepted scientific naming conventions.",
                }
            },
            "date_outlier_kmeans": {
                "namespace": Namespace("http://example.com/vocab/date_outlier_kmeans/"),
                "assess_namespace": URIRef("http://example.com/assess/date_outlier_kmeans/"),
                "prefix": "date_outlier_kmeans",
                "labels": {
                    "outlier_date": "This label is used to tag dates that are determined to be significantly different from the majority, based on the KMeans clustering algorithm. Such dates fall into the smallest cluster or are far from the centroids of their clusters, indicating they deviate notably from typical date values.",
                    "normal_date": "This label is applied to dates that are considered to be within the expected range, based on the KMeans clustering results. These dates fall into larger clusters and are close to the centroids, indicating they align with the common patterns observed in the dataset.",
                }
            },
            "date_outlier_irq": {
                "namespace": Namespace("http://example.com/vocab/date_outlier_irq/"),
                "assess_namespace": URIRef("http://example.com/assess/date_outlier_irq/"),
                "prefix": "date_outlier_irq",
                "labels": {
                    "outlier_date": "This label indicates that the observation date significantly deviates from the typical range, suggesting it may be an anomaly. (Based on IRQ Method)",
                    "normal_date": "This label indicates that the observation date falls within the typical range, suggesting it is not an anomaly. (Based on IRQ Method)",
                },
            },
            "point_outlier_irq": {
                "namespace": Namespace("http://example.com/vocab/point_outlier_irq/"),
                "assess_namespace": URIRef("http://example.com/assess/point_outlier_irq/"),
                "prefix": "point_outlier_irq",
                "labels": {
                    "outlier_point": "This label indicates that the observation point significantly deviates from the typical range, suggesting it may be an anomaly. (Based on IRQ Method)",
                    "normal_point": "This label indicates that the observation point falls within the typical range, suggesting it is not an anomaly. (Based on IRQ Method)",
                }
            },
            "point_outlier_zscore": {
                "namespace": Namespace("http://example.com/vocab/point_outlier_zscore/"),
                "assess_namespace": URIRef("http://example.com/assess/point_outlier_zscore/"),
                "prefix": "point_outlier_zscore",
                "labels": {
                    "outlier_point": "This label indicates that the observation point significantly deviates from the typical range, suggesting it may be an anomaly. (Based on Z-Score Method)",
                    "normal_point": "This label indicates that the observation point falls within the typical range, suggesting it is not an anomaly. (Based on Z-Score Method)",
                },
            },
            "datum_is_empty": {
                "namespace": Namespace("http://example.com/vocab/datum_is_empty/"),
                "assess_namespace": URIRef("http://example.com/assess/datum_is_empty/"),
                "prefix": "datum_is_empty",
                "labels": {
                    "empty": "Indicates that the datum link reference is empty.",
                    "not_empty": "Indicates that the datum link reference is not empty.",
                },
            },

            "date_is_empty": {
                "namespace": Namespace("http://example.com/vocab/date_is_empty/"),
                "assess_namespace": URIRef("http://example.com/assess/date_is_empty/"),
                "prefix": "date_is_empty",
                "labels": {
                    "empty": "Indicates that the date is empty.",
                    "non_empty": "Indicates that the date is not empty.",
                },
            },
            "datum_validation": {
                "namespace": Namespace("http://example.com/vocab/datum_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/datum_validation/"),
                "prefix": "datum_validation",
                "labels": {
                    "valid": "Indicates that the datum link reference is valid and recognized.",
                    "invalid": "Indicates that the datum link reference is invalid or unrecognized.",
                },
            },
            "datum_type": {
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
            },
            "date_format_validation": {
                "namespace": Namespace("http://example.com/vocab/date_format_validation/"),
                "assess_namespace": URIRef("http://example.com/assess/date_format_validation/"),
                "prefix": "date_format_validation",
                "labels": {
                    "valid": "Indicates that the date format is valid and recognized.",
                    "invalid": "Indicates that the date format is invalid or unrecognized.",
                },
            },
            "coordinate_precision": {
                "namespace": Namespace("http://example.com/vocab/coordinate_precision/"),
                "assess_namespace": URIRef("http://example.com/assess/coordinate_precision/"),
                "prefix": "coordinate_precision",
                "labels": {
                    "Low": "Indicates low precision in coordinate values if latitude or longitude of the location point has less than 2 decimal point.",
                    "Medium": "Indicates medium precision in coordinate values if latitude or longitude of the location point has between 2 and 4 decimal point.",
                    "High": "Indicates high precision in coordinate values if latitude or longitude of the location point has more than 4 decimal point.",
                },
            },
            "australia_state": {
                "namespace": Namespace("http://example.com/vocab/australia_state/"),
                "assess_namespace": URIRef("http://example.com/assess/australia_state/"),
                "prefix": "australia_state",
                "labels": {
                    "New_South_Wales": "Indicates that the point is in New South Wales, a state on the east coast of Australia.",
                    "Victoria": "Indicates that the point is in Victoria, a state in southeast Australia.",
                    "Queensland": "Indicates that the point is in Queensland, a state in northeast Australia.",
                    "Western_Australia": "Indicates that the point is in Western Australia, a state occupying the entire western third of Australia.",
                    "South_Australia": "Indicates that the point is in South Australia, a state in the southern central part of Australia.",
                    "Tasmania": "Indicates that the point is in Tasmania, an island state off the southern coast of Australia.",
                    "Northern_Territory": "Indicates that the point is in the Northern Territory, a federal Australian territory in the center and central northern regions.",
                    "Australian_Capital_Territory": "Indicates that the point is in the Australian Capital Territory, Australia's federal district, located in the southeast of the country.",
                    "Outside_Australia": "Indicates that the point is outside the geographical bounds of Australia.",
                },
            },
        }

    def get_namespaces(self, namespace_key):
        if namespace_key in self.namespaces_and_labels:
            return self.namespaces_and_labels[namespace_key]["namespace"], self.namespaces_and_labels[namespace_key][
                "assess_namespace"]
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
        # Generate the labels list in 'prefix:label' format
        labels_with_prefix = self.get_all_labels()

        # Create a DataFrame with one column for 'Usecase' and others for each label
        # Initially, all values except the column headers are empty
        columns = ['Usecase'] + labels_with_prefix
        df = pd.DataFrame(columns=columns)

        # Optionally, add example data or leave it blank

        # Save the DataFrame to an Excel file
        df.to_excel(output_filename, index=False)
        print(f"Excel template has been created: {output_filename}")

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

    def bind_standard_namespaces(self, graph=None):
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
