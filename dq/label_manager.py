from rdflib import Graph, Namespace, Literal
from rdflib.namespace import SKOS, RDF


class LabelManager:
    def __init__(self):

        self.g = Graph()
        self.namespaces_and_labels = {
            "date_recency": {
                "namespace": Namespace("http://example.org/vocab/date_recency/"),
                "prefix": "date_r",
                "labels": {
                    "recent": "This label indicates that the observation date is within the last 20 years, making it more relevant to current contexts and studies.",
                    "outdated": "This label indicates that the observation date is more than 20 years ago, before 20 years, and may not reflect the current state or conditions.",
                },
            },
            "outlier_date": {
                "namespace": Namespace("http://example.org/vocab/outlier_date_assessment/"),
                "prefix": "out_d",
                "labels": {
                    "outlier_date": "This label indicates that the observation date significantly deviates from the typical range, suggesting it may be an anomaly.",
                    "normal_date": "This label indicates that the observation date falls within the typical range, suggesting it is not an anomaly.",
                },
            },
            "outlier_point": {
                "namespace": Namespace("http://example.org/vocab/outlier_point_assessment/"),
                "prefix": "out_p",
                "labels": {
                    "outlier_point": "This label indicates that the observation point significantly deviates from the typical range, suggesting it may be an anomaly.",
                    "normal_point": "This label indicates that the observation point falls within the typical range, suggesting it is not an anomaly.",
                },
            },

            "date_validation": {
                "namespace": Namespace("http://example.org/vocab/date_validation/"),
                "prefix": "date_v",
                "labels": {
                    "valid": "Indicates that the date format is valid and recognized.",
                    "invalid": "Indicates that the date format is invalid or unrecognized.",
                },
            },
            "coordinate_precision": {
                "namespace": Namespace("http://example.org/vocab/coordinate_precision/"),
                "prefix": "cor_p",
                "labels": {
                    "Low": "Indicates low precision in coordinate values if latitude or longitude of the location point has less than 2 decimal point.",
                    "Medium": "Indicates medium precision in coordinate values if latitude or longitude of the location point has between 2 and 4 decimal point.",
                    "High": "Indicates high precision in coordinate values if latitude or longitude of the location point has more than 4 decimal point.",
                },
            },
            "australia_state": {
                "namespace": Namespace("http://example.org/vocab/australia_state/"),
                "prefix": "aus_st",
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

    def get_namespace(self, namespace_key):
        if namespace_key in self.namespaces_and_labels:
            return self.namespaces_and_labels[namespace_key]["namespace"]
        else:
            raise KeyError(f"Namespace '{namespace_key}' not found in the namespaces_and_labels dictionary.")

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
