import re
from collections import defaultdict
from typing import Dict

from rdflib import Graph, URIRef, Literal


class ReportAnalysis:
    def __init__(self, g: Graph, report_file=None):
        self.g = g
        self.report_file = report_file

    @staticmethod
    def extract_namespace(uri):
        uri_str = str(uri)
        match = re.match(r'^(.*[#/])', uri_str)
        if match:
            return match.group(1)
        return uri_str

    def namespace_frequencies(self):
        ns_freq = defaultdict(int)

        for s, p, o in self.g:
            if isinstance(s, URIRef):
                ns_freq[self.extract_namespace(s)] += 1
            if isinstance(p, URIRef):
                ns_freq[self.extract_namespace(p)] += 1
            if isinstance(o, URIRef):
                ns_freq[self.extract_namespace(o)] += 1

        sorted_ns_freq = sorted(ns_freq.items(), key=lambda item: item[1], reverse=True)
        return sorted_ns_freq

    def get_sorted_namespaces(self):
        frequencies = self.namespace_frequencies()

        sorted_namespaces = []
        for ns_uri, freq in frequencies:
            prefix = [prefix for prefix, uri in self.g.namespaces() if str(uri) == ns_uri]
            if prefix:
                sorted_namespaces.append((prefix[0], ns_uri, freq))
            else:
                sorted_namespaces.append((None, ns_uri, freq))

        return sorted_namespaces

    def analyze_unique_predicates(self) -> Dict[str, int]:
        predicates = set(self.g.predicates())
        return {str(p): sum(1 for _ in self.g.triples((None, p, None))) for p in predicates}

    def predicate_value_assessment(self) -> Dict[str, Dict[str, int]]:
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
        total_triples = len(self.g)
        unique_subjects = len(set(self.g.subjects()))
        unique_predicates = len(set(self.g.predicates()))
        unique_objects = len(set(self.g.objects()))
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

                print(f" {predicate_index} - {str(predicate)}: {count}", file=self.report_file)

            sorted_namespaces = self.get_sorted_namespaces()
            print(f"========= Namespaces ({len(sorted_namespaces)})===============", file=self.report_file)
            print(f" # - Prefix (Frequency): URI ", file=self.report_file)
            i = 0
            for prefix, uri, freq in sorted_namespaces:
                i += 1
                print(f"{i}- {prefix if prefix else 'No prefix'} ({freq}): {uri} ",
                      file=self.report_file)

        print(f"", file=self.report_file)
        print(f"--->>> Assessment Report <<<---", file=self.report_file)

    def calculate_predicate_completeness(self, predicate_uri):
        if isinstance(predicate_uri, str):
            predicate_uri = URIRef(predicate_uri)

        subjects_with_predicate = set(self.g.subjects(predicate=predicate_uri))

        all_relevant_subjects = subjects_with_predicate

        if len(all_relevant_subjects) > 0:
            completeness = len(subjects_with_predicate) / len(all_relevant_subjects)
        else:
            completeness = 0

        return completeness
