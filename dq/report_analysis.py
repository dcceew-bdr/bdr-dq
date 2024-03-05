import re
from collections import defaultdict
from typing import Dict

from rdflib import Graph, URIRef, Literal

from .defined_namespaces import uri_to_prefix


class ReportAnalysis:
    def __init__(self, g: Graph, report_file=None):
        self.g = g
        self.report_file = report_file

    @staticmethod
    def extract_namespace(uri):
        """
        Extracts the namespace from a given URIRef object by finding the substring
        up to the last occurrence of '#' or '/'.
        """
        # Convert URIRef to string if not already
        uri_str = str(uri)
        # Find the last occurrence of '#' or '/'
        match = re.match(r'^(.*[#/])', uri_str)
        if match:
            return match.group(1)
        return uri_str  # Return the original string if no '#' or '/' found

    def namespace_frequencies(self):
        """
        Count the frequencies of each namespace in the graph.
        """
        ns_freq = defaultdict(int)

        for s, p, o in self.g:
            if isinstance(s, URIRef):
                ns_freq[self.extract_namespace(s)] += 1
            if isinstance(p, URIRef):
                ns_freq[self.extract_namespace(p)] += 1
            if isinstance(o, URIRef):
                ns_freq[self.extract_namespace(o)] += 1

        # Sort by frequency in descending order
        sorted_ns_freq = sorted(ns_freq.items(), key=lambda item: item[1], reverse=True)
        return sorted_ns_freq

    def get_sorted_namespaces(self):
        """
        Returns namespaces sorted by their frequency of appearance in descending order.

        Each item in the list is a tuple containing (prefix, namespace URI, frequency).
        """
        # Get the frequencies of each namespace
        frequencies = self.namespace_frequencies()

        # Match the namespace URIs to their prefixes
        sorted_namespaces = []
        for ns_uri, freq in frequencies:
            # Find the prefix for the namespace URI
            prefix = [prefix for prefix, uri in self.g.namespaces() if str(uri) == ns_uri]
            if prefix:
                sorted_namespaces.append((prefix[0], ns_uri, freq))
            else:
                sorted_namespaces.append((None, ns_uri, freq))

        return sorted_namespaces

    def get_namespaces(self):
        """
        Returns a list of all namespace names and URLs from the graph.

        Returns:
            List of tuples, each containing (prefix, namespace URI).
        """
        # Accessing the namespaces from the graph and returning them
        return list(self.g.namespaces())

    def analyze_unique_predicates(self) -> Dict[str, int]:
        """Identify and count unique predicates."""
        predicates = set(self.g.predicates())
        return {str(p): sum(1 for _ in self.g.triples((None, p, None))) for p in predicates}

    def predicate_value_assessment(self) -> Dict[str, Dict[str, int]]:
        """
        Assess predicates for values that are non-empty versus empty.
        Empty values are considered as None or empty strings.
        """
        predicate_assessment = {}
        for predicate in set(self.g.predicates()):
            predicate_assessment[str(predicate)] = {"non_empty": 0, "empty": 0}
            for _, _, obj in self.g.triples((None, predicate, None)):
                if obj is None or (isinstance(obj, Literal) and not obj.strip()):
                    predicate_assessment[str(predicate)]["empty"] += 1
                else:
                    predicate_assessment[str(predicate)]["non_empty"] += 1
        return predicate_assessment

    def generate_report(self):
        # Count the total number of triples
        total_triples = len(self.g)
        # Count unique subjects, predicates, and objects
        unique_subjects = len(set(self.g.subjects()))
        unique_predicates = len(set(self.g.predicates()))
        unique_objects = len(set(self.g.objects()))
        # Generate the report
        report = (f"The RDF file you've provided contains {total_triples} triples, "
                  f"which are the basic units of information in RDF, composed of "
                  f"a subject, predicate, and object. It includes {unique_subjects} "
                  f"unique subjects, {unique_predicates} unique predicates, and "
                  f"{unique_objects} unique objects.")

        if self.report_file:
            print("** RDF Data Quality Assessment Report **", file=self.report_file)
            print("========================================", file=self.report_file)

            print(report, file=self.report_file)

            unique_predicates = self.analyze_unique_predicates()

            print(f"=========  Unique Predicates ({len(unique_predicates.items())})===============",
                  file=self.report_file)
            predicate_index = 0
            for predicate, count in unique_predicates.items():
                predicate_index += 1
                predicate_short = uri_to_prefix(str(predicate))

                print(f" {predicate_index} - {predicate_short}: {count}", file=self.report_file)

            sorted_namespaces = self.get_sorted_namespaces()
            print(f"========= Namespaces ({len(sorted_namespaces)})===============", file=self.report_file)
            # Printing the list of namespaces
            print(f" # - Prefix (Frequency): URI ", file=self.report_file)
            i = 0
            for prefix, uri, freq in sorted_namespaces:
                i += 1
                print(f"{i}- {prefix if prefix else 'No prefix'} ({freq}): {uri} ",
                      file=self.report_file)

        print(f"", file=self.report_file)
        print(f"--->>> Assessment Report <<<---", file=self.report_file)

    def calculate_predicate_completeness(self, predicate_uri):
        """
        Calculate the completeness of a given predicate in the graph.

        Completeness is defined as the ratio of the number of subjects with the predicate
        to the total number of unique subjects.

        :param predicate_uri: The URI of the predicate to calculate completeness for.
        :return: Completeness ratio.
        """
        # Ensure predicate_uri is a URIRef object
        if isinstance(predicate_uri, str):
            predicate_uri = URIRef(predicate_uri)

        # Get subjects that have the specified predicate (with values)
        subjects_with_predicate = set(self.g.subjects(predicate=predicate_uri))

        # In this specific context, all subjects relevant to the predicate are those that have the predicate,
        # since we are only considering those subjects that are associated with the predicate.
        # If there's a way to determine subjects that should have the predicate but don't,
        # that logic would need to be added here.
        all_relevant_subjects = subjects_with_predicate

        # Calculate completeness
        if len(all_relevant_subjects) > 0:
            completeness = len(subjects_with_predicate) / len(all_relevant_subjects)
        else:
            completeness = 0  # Define completeness as 0 if there are no subjects at all

        return completeness
