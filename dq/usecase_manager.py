import pandas as pd
import rdflib
from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

from label_manager import LabelManager


class UseCaseManager:
    def __init__(self, excel_file, results_ttl):
        self.excel_file = excel_file
        self.results_ttl = results_ttl
        self.use_cases_df = None
        self.results_graph = rdflib.Graph()
        self.label_manager = LabelManager()
        self.use_case_matrix = {}

    def read_excel(self):
        """Reads the Excel file with use case definitions into a DataFrame."""
        self.use_cases_df = pd.read_excel(self.excel_file)

    def load_rdf_results(self):
        """Loads the RDF data from the .ttl file."""
        self.results_graph.parse(self.results_ttl, format="turtle")

    def create_use_case_matrix(self):
        """Creates a matrix based on the use case definitions and labels."""
        # No need to fetch all labels if we directly use the ones defined in the Excel file
        # Reading labels (excluding the first column which is assumed to be use case names)
        labels = self.use_cases_df.columns[1:]

        # Initialize the use case matrix with conditions from the Excel file
        self.use_case_matrix = {}
        for index, row in self.use_cases_df.iterrows():
            use_case = row['Usecase']  # Assuming the first column is named 'Usecase'
            self.use_case_matrix[use_case] = {}
            for label in labels:
                # Set to True if the cell contains 1, False otherwise (including 0 or empty)
                self.use_case_matrix[use_case][label] = True if row[label] == 1 else False
        print("Use Case Matrix")
        print(self.use_case_matrix)

    def assess_use_cases(self):
        """Assesses each use case based on the RDF data."""
        for _, row in self.use_cases_df.iterrows():
            use_case = row.iloc[0]
            for label in self.use_case_matrix[use_case].keys():
                if row.get(label, 0) == 1:
                    self.use_case_matrix[use_case][label] = self.check_label_in_results(label)

    def check_label_in_results(self, label):
        """Checks if a label is present in the RDF results."""
        for s, p, o in self.results_graph:
            if str(p).endswith(label):  # Simplistic check; might need refinement based on actual RDF structure
                return True
        return False

    def write_results_to_ttl(self, output_ttl_file):
        """Writes the final use case results to a new .ttl file."""
        new_graph = rdflib.Graph()
        ns = Namespace("http://example.com/usecases/")
        for use_case, labels in self.use_case_matrix.items():
            use_case_uri = ns[use_case]
            for label, result in labels.items():
                if result:
                    # Add triples to indicate a use case includes a specific label based on assessment
                    label_uri = ns[label.replace(':', '_')]  # Simplify label to URI-safe format
                    new_graph.add((use_case_uri, RDF.type, label_uri))
                    new_graph.add((use_case_uri, RDFS.label, Literal(use_case)))
                    new_graph.add((label_uri, RDFS.label, Literal(label)))
        new_graph.serialize(destination=output_ttl_file, format='turtle')
        print(f"Results written to {output_ttl_file}")
