import datetime
from datetime import datetime

import numpy as np
import pandas as pd
import rdflib
from rdflib import URIRef, Literal, BNode, SOSA, SDO, XSD

from .defined_namespaces import DQAF
from .vocab_manager import VocabManager


class ScoringManager:
    def __init__(self, scoring_definition_excel_file, assess_matrix_df, results_ttl, output_result_file,
                 report_file=None):
        self.scoring_definition_excel_file = scoring_definition_excel_file
        self.output_result_file = output_result_file
        self.report_file = report_file
        self.scoring_df = None
        self.results_ttl = results_ttl
        self.results_graph = rdflib.Graph()
        self.results_graph.parse(self.results_ttl, format="turtle")
        self.label_manager = VocabManager()
        self.scoring_matrix = {}
        self.create_scoring_matrix()
        self.result_matrix_df = assess_matrix_df

    def create_scoring_matrix(self):
        self.scoring_df = pd.read_excel(self.scoring_definition_excel_file, sheet_name="Weighing")
        header = 0
        self.scoring_df = self.scoring_df.set_index('Data quality assertion').T.reset_index()

        self.scoring_matrix = {}

        for _, row in self.scoring_df.iterrows():
            scoring_dict = row.to_dict()
            row_name = scoring_dict.pop('index')
            self.scoring_matrix[row_name] = scoring_dict

        print("Scoring Matrix:")
        print(self.scoring_matrix)

    @staticmethod
    def extract_record_number(record_uri):
        try:
            return int(record_uri.split('/')[-1])
        except ValueError:
            return None

    def apply_scoring_methods(self):

        for scoring_method, conditions in self.scoring_matrix.items():
            assessment_name = "Scoring Method Applying: " + scoring_method
            total_assessments = 0
            result_counts = {'Max': 0, 'Min': 0, 'Avg': 0}

            scoring_results = []
            scoring_vector, scoring_keys = dictionary_to_vector_and_keys(conditions)


            for _, row in self.result_matrix_df.iterrows():

                row_vector = [1 if row[key] == 1.0 else 0 for key in scoring_keys]
                dot_product = np.dot(scoring_vector, row_vector)
                formatted_mapped_value = f"{dot_product:.4f}"

                scoring_results.append(float(formatted_mapped_value))


            min_score = min(scoring_results)
            max_score = max(scoring_results)

            print('Scoring Min, Max', min_score,max_score)
            if max_score == min_score:
                raise ValueError("max_score must be greater than min_score")


            scoring_results = []
            for _, row in self.result_matrix_df.iterrows():
                total_assessments += 1
                row_vector = [1 if row[key] == 1.0 else 0 for key in scoring_keys]
                dot_product = np.dot(scoring_vector, row_vector)

                mapped_value = (dot_product - min_score) / (max_score - min_score)
                formatted_mapped_value = f"{mapped_value:.4f}"

                scoring_results.append(float(formatted_mapped_value))

                self._add_scoring_result(scoring_method, row['observation_id'], formatted_mapped_value)

            self.result_matrix_df[scoring_method] = scoring_results
            result_counts['Min'] = min(scoring_results)
            result_counts['Avg'] = sum(scoring_results) / len(scoring_results) if scoring_results != 0 else 'NA'
            result_counts['Max'] = max(scoring_results)



            self.add_to_report(assessment_name, total_assessments, result_counts)

        self.results_graph.serialize(destination=self.output_result_file, format="turtle")

    def _add_scoring_result(self, scoring_method, observation_id, value, scoring_date=None):
        subject = URIRef(f"http://example.com/scoring_assessment/{scoring_method}/{observation_id}")
        assessment_type = URIRef(f"http://example.com/scoring_assessment/{scoring_method}/")
        result_bn = BNode()
        self.results_graph.add((subject, DQAF.hasDQAFResult, result_bn))
        self.results_graph.add((result_bn, SOSA.observedProperty, assessment_type))

        self.results_graph.add((result_bn, SDO.value, Literal(value)))
        if scoring_date is None:
            scoring_date = datetime.now()
        elif isinstance(scoring_date, datetime.date) and not isinstance(scoring_date, datetime.datetime):
            scoring_date = datetime.datetime.combine(scoring_date, datetime.time.min)

        self.results_graph.add((result_bn, SOSA.resultTime, Literal(scoring_date, datatype=XSD.dateTime)))

    def add_to_report(self, scoring_name, total_scoring_applied, result_counts):
        if self.report_file:
            print(f'', file=self.report_file)
            print(f'- {scoring_name}: {total_scoring_applied}', file=self.report_file)
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
    vector = [v if v else 0 for v in flat_dict.values()]
    keys = list(flat_dict.keys())
    return vector, keys


def calculate_subgroup_max_score(dictionary):
    grouped_values = {}
    for key, value in dictionary.items():
        main_group, _ = key.split(':', 1)
        if main_group in grouped_values:
            grouped_values[main_group] = max(grouped_values[main_group], value)
        else:
            grouped_values[main_group] = value
    return sum(grouped_values.values())

def calculate_subgroup_min_score(dictionary):
    grouped_values = {}
    for key, value in dictionary.items():
        main_group, _ = key.split(':', 1)
        if main_group in grouped_values:
            grouped_values[main_group] = min(grouped_values[main_group], value)
        else:
            grouped_values[main_group] = value
    return sum(grouped_values.values())