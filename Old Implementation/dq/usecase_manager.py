import datetime
from datetime import datetime
import re
import numpy as np
import pandas as pd
import rdflib
from rdflib import URIRef, Literal, BNode, SOSA, SDO, XSD

from .defined_namespaces import DQAF
from .vocab_manager import VocabManager


class UseCaseManager:
    def __init__(self, use_case_definition_excel_file, assess_matrix_df, results_ttl, output_result_file,
                 report_file=None):
        self.use_case_definition_excel_file = use_case_definition_excel_file
        self.output_result_file = output_result_file
        self.report_file = report_file
        self.use_cases_df = None
        self.results_ttl = results_ttl
        self.results_graph = rdflib.Graph()
        self.results_graph.parse(self.results_ttl, format="turtle")
        self.label_manager = VocabManager()
        self.use_case_matrix = {}
        self.create_use_case_matrix()
        self.result_matrix_df = assess_matrix_df

    def create_use_case_matrix(self):
        self.use_cases_df = pd.read_excel(self.use_case_definition_excel_file, sheet_name="Use case template")
        header = 0
        self.use_cases_df = self.use_cases_df.set_index('Data quality assertion').T.reset_index()

        self.use_case_matrix = {}

        for _, row in self.use_cases_df.iterrows():
            use_cases_dict = row.to_dict()
            row_name = use_cases_dict.pop('index')
            self.use_case_matrix[row_name] = use_cases_dict

        for key, subdict in self.use_case_matrix.items():
            for subkey, value in subdict.items():
                if value != value:
                    self.use_case_matrix[key][subkey] = 0
                elif value == 1.0:
                    self.use_case_matrix[key][subkey] = 1

        print("Use Case Matrix:")
        print(self.use_case_matrix)

    @staticmethod
    def extract_record_number(record_uri):
        patterns = [r"http://createme.org/attribute/basisOfRecord/(\d+)",
         r"http://createme.org/attribute/kingdom/(\d+)",
         r"http://createme.org/observation/scientificName/(\d+)",
         r"http://createme.org/sample/field/(\d+)",
         r"http://createme.org/sample/specimen/(\d+)",
         r"http://createme.org/sampling/field/(\d+)",
         r"http://createme.org/sampling/specimen/(\d+)",
         r"http://createme.org/scientificName/(\d+)",
         r"http://createme.org/scientificName/(\d+)/observationNameMatch",
         r"http://createme.org/scientificName/(\d+)/taxon",
         r"http://createme.org/value/basisOfRecord/(\d+)",
         r"http://createme.org/value/kingdom/(\d+)"]

        for pattern in patterns:
            match = re.match(pattern, record_uri)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    return None
        return None

    def assess_use_cases(self):

        for use_case, conditions in self.use_case_matrix.items():
            assessment_name = "Use Case Assessment: " + use_case
            total_assessments = 0
            result_counts = {'True': 0, 'False': 0}

            use_case_results = []
            use_case_vector, use_case_keys = dictionary_to_vector_and_keys(conditions)
            use_case_sum = calculate_subgroup_sums(conditions)

            for _, row in self.result_matrix_df.iterrows():
                total_assessments += 1
                row_vector = [1 if row[key] == 1.0 else 0 for key in use_case_keys]
                dot_product = np.dot(use_case_vector, row_vector)
                use_case_satisfied = use_case_sum == dot_product
                use_case_results.append(use_case_satisfied)
                label = "True" if use_case_satisfied else "False"
                result_counts[label] += 1

                self._add_use_case_assessment_result(use_case, row['observation_id'], use_case_satisfied)

            self.result_matrix_df[use_case] = use_case_results
            self.add_to_report(assessment_name, total_assessments, result_counts)

        self.results_graph.serialize(destination=self.output_result_file, format="turtle")
        print(self.output_result_file)

    def _add_use_case_assessment_result(self, use_case, observation_id, value, assessment_date=None):
        subject = URIRef(f"http://example.com/use_case_assessment/{use_case}/{observation_id}")
        assessment_type = URIRef(f"http://example.com/use_case_assessment/{use_case}/")
        result_bn = BNode()
        self.results_graph.add((subject, DQAF.hasDQAFResult, result_bn))
        self.results_graph.add((result_bn, SOSA.observedProperty, assessment_type))

        self.results_graph.add((result_bn, SDO.value, Literal(value)))
        if assessment_date is None:
            assessment_date = datetime.now()
        elif isinstance(assessment_date, datetime.date) and not isinstance(assessment_date, datetime.datetime):
            assessment_date = datetime.datetime.combine(assessment_date, datetime.time.min)

        self.results_graph.add((result_bn, SOSA.resultTime, Literal(assessment_date, datatype=XSD.dateTime)))

    def add_to_report(self, assessment_name, total_assessments, result_counts):
        if self.report_file:
            print(f'', file=self.report_file)
            print(f'- {assessment_name}: {total_assessments}', file=self.report_file)
            for quality, count in result_counts.items():
                print(f'\t{quality}: {count}', file=self.report_file)


def flatten_dictionary(dictionary, parent_key='', sep='_'):
    items = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def dictionary_to_vector_and_keys(dictionary):
    flat_dict = flatten_dictionary(dictionary)
    vector = [1 if v else 0 for v in flat_dict.values()]
    keys = list(flat_dict.keys())
    return vector, keys


def calculate_subgroup_sums(dictionary):
    grouped_values = {}
    for key, value in dictionary.items():
        main_group, _ = key.split(':', 1)
        if main_group in grouped_values:
            grouped_values[main_group] = max(grouped_values[main_group], value)
        else:
            grouped_values[main_group] = value
    return sum(grouped_values.values())
