import pandas as pd
import rdflib
from rdflib import URIRef, Literal, Namespace, BNode, SOSA, SDO, XSD
from rdflib.namespace import RDF, RDFS, FOAF
from .defined_namespaces import DQAF, TERN
from .vocab_manager import VocabManager
from rdflib.namespace import DCTERMS

import datetime
from datetime import datetime
def split_uri_into_prefix_and_label(graph, uri):
    """
    Splits a given URI into a prefix and a label based on the namespaces registered in the graph.

    Args:
        graph (rdflib.Graph): The RDF graph with registered namespaces.
        uri (str): The full URI to split.

    Returns:
        tuple: A tuple containing the prefix (or the full namespace URI if no direct prefix match) and the label.
    """
    if not isinstance(uri, rdflib.URIRef):
        uri = rdflib.URIRef(uri)

    # Initialize the longest match to an empty string
    longest_match = ""
    matched_prefix = None

    # Iterate through registered namespaces in the graph
    for prefix, namespace in graph.namespace_manager.namespaces():
        ns_str = str(namespace)
        if str(uri).startswith(ns_str) and len(ns_str) > len(longest_match):
            longest_match = ns_str
            matched_prefix = prefix

    if longest_match:
        # Extract the label part of the URI by removing the namespace
        label = str(uri)[len(longest_match):]
        return (matched_prefix, label)
    else:
        # If there's no matching namespace, return None for the prefix
        return (None, str(uri))


def get_prefix_for_uri(graph, uri):
    """
    Finds the prefix for a given URI based on the namespaces registered in the graph.

    Args:
        graph (rdflib.Graph): The RDF graph.
        uri (str): The URI for which to find the prefix.

    Returns:
        str: The prefix associated with the URI, or None if not found.
    """
    # Convert the URI to an rdflib.URIRef object if it's not already one
    if not isinstance(uri, rdflib.URIRef):
        uri = rdflib.URIRef(uri)

    # Iterate through registered namespaces in the graph
    for prefix, namespace in graph.namespace_manager.namespaces():
        if uri.startswith(namespace):
            return prefix  # Return the prefix if the URI starts with the namespace

    return None  # Return None if no matching namespace is found


class UseCaseManager:
    def __init__(self, excel_file, results_ttl):
        self.excel_file = excel_file
        self.results_ttl = results_ttl
        self.use_cases_df = None
        self.results_graph = rdflib.Graph()
        self.label_manager = VocabManager()
        self.use_case_matrix = {}

    def read_excel(self):
        """Reads the Excel file with use case definitions into a DataFrame."""
        self.use_cases_df = pd.read_excel(self.excel_file,sheet_name="Use case template")

    def load_rdf_results(self):
        """Loads the RDF data from the .ttl file."""
        self.results_graph.parse(self.results_ttl, format="turtle")

    def create_use_case_matrix(self):
        """Creates a matrix based on the use case definitions and labels."""
        # No need to fetch all labels if we directly use the ones defined in the Excel file
        # Reading labels (excluding the first column which is assumed to be use case names)
        #labels = self.use_cases_df.columns[1:]
        use_cases=self.use_cases_df.columns[1:]
        self.use_case_matrix ={}
        for use_case in use_cases:
            self.use_case_matrix[use_case]= {}
        # Initialize the use case matrix with conditions from the Excel file

        for index, row in self.use_cases_df.iterrows():
            label = row['Data quality assertion']  # Assuming the first column is named 'Data quality assertion'
            for use_case in use_cases:
                # Set to True if the cell contains 1, False otherwise (including 0 or empty)
                self.use_case_matrix[use_case][label] = True if row[use_case] == 1 else False
        print("Use Case Matrix")
        print(self.use_case_matrix)


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
                # print(label, result)
                if result:
                    # Add triples to indicate a use case includes a specific label based on assessment
                    label_uri = ns[label.replace(':', '_')]  # Simplify label to URI-safe format
                    new_graph.add((use_case_uri, RDF.type, label_uri))
                    new_graph.add((use_case_uri, RDFS.label, Literal(use_case)))
                    new_graph.add((label_uri, RDFS.label, Literal(label)))
        new_graph.serialize(destination=output_ttl_file, format='turtle')
        print(f"Results written to {output_ttl_file}")


class TurtleToExcelConverter:
    def __init__(self, input_result_file, use_case_definition_file, output_result_file):
        self.input_result_file = input_result_file
        self.use_case_definition_file = use_case_definition_file
        self.output_result_file = output_result_file

        self.manager = UseCaseManager(self.use_case_definition_file, self.input_result_file)
        self.manager.read_excel()
        self.manager.load_rdf_results()
        self.manager.create_use_case_matrix()

        # self.manager.assess_use_cases()
        # self.manager.write_results_to_ttl(output_result_file)

    def uri_to_label(self, uri):
        # Mapping URI prefixes to meaningful labels
        mappings = {
            "http://createme.org/observation/individualCount/": 'Observation_Count',
            "http://createme.org/attribute/kingdom/": 'Attribute_Kingdom',
            "http://createme.org/observation/scientificName/": 'Observation_Scientific_Name',
            "http://createme.org/provider/": 'Provider',
            "http://createme.org/sample/field/": 'Sample_Field',
            "http://createme.org/sampling/field/": 'sampling_field',
            "http://createme.org/scientificName/": 'Scientific_Name',
            "http://createme.org/value/individualCount/": "Individual_Count",
            "http://createme.org/value/kingdom/": "value_kingdom",

        }
        # Check if the URI starts with one of the defined prefixes and replace accordingly
        for prefix, label in mappings.items():

            if str(uri).startswith(prefix):
                # Return the label
                return label  # + '_' + str(uri)[len(prefix):]
        # Default: return the URI as is if no prefix matches
        return str(uri)

    def parse_turtle(self):
        g = rdflib.Graph()
        g.parse(self.input_result_file, format="turtle")

        # Initialize a dictionary to hold the data for each record, keyed by record number
        records = {}

        # Extract all URIs related to records specified by dcterms:hasPart
        for _, _, record_uri in g.triples((None, DCTERMS.hasPart, None)):
            # Extract the record number from the URI
            record_number = self.extract_record_number(record_uri)
            label = self.uri_to_label(record_uri)

            if record_number is not None:
                if record_number not in records:
                    records[record_number] = {}

                # For each related URI, extract additional data and organize it under the record number
                for subj, pred, obj in g.triples((record_uri, None, None)):
                    # Simplify the predicate URI for use as a column header

                    column_header = pred.split('/')[-1]
                    # Store the object as data for the record, under the appropriate column
                    # Check if obj is a literal value, a URI node, or a Blank Node
                    if isinstance(obj, rdflib.Literal):
                        # Literal values can be converted directly to string
                        value = str(obj)
                        records[record_number][label + "_" + column_header] = value
                    elif isinstance(obj, rdflib.URIRef) or isinstance(obj, rdflib.BNode):
                        for s2, p2, value2 in g.triples((obj, None, None)):

                            prefix = get_prefix_for_uri(g, p2)
                            if isinstance(value2, rdflib.Literal):
                                records[record_number][label + "_" + column_header + "#" + str(prefix)] = str(value2)
                            else:
                                prefix2, label2 = split_uri_into_prefix_and_label(g, value2)
                                if prefix2 is not None:
                                    records[record_number][prefix2] = label2

                                # print(label, s2, prefix, prefix2, label2)

                        # For URIRefs/BNodes, you might want to handle them differently
                        # This could involve fetching additional details from the graph,
                        # or simply storing the URI string. Adjust as needed.
                        # value = "Nested --> " + str(obj)  # Placeholder: adjust based on how you want to handle nodes

        # Convert the records dictionary to a DataFrame
        data = [dict(record_id=k, **v) for k, v in sorted(records.items(), key=lambda item: item[0])]
        df = pd.DataFrame(data)

        # assess use case
        df = df.sort_values(by='record_id', ascending=True)
        df = self.assess_use_cases(df, self.manager.use_case_matrix)

        return df

    def extract_record_number(self, record_uri):
        try:
            return int(record_uri.split('/')[-1])
        except ValueError:
            return None

    def assess_use_cases(self, df, use_case_matrix):
        for use_case, conditions in use_case_matrix.items():
            # Initialize a list to store the results for this use case across all records
            use_case_results = []

            for _, row in df.iterrows():
                # Assume the use case is satisfied unless a condition fails
                use_case_satisfied = True

                for condition, expected_value in conditions.items():
                    if expected_value:
                        column_name, condition_value = condition.split(":")
                        # Check the values of a specific label in lower case 
                        actual_value = row[column_name].lower() == condition_value.lower()

                        # If the condition does not match the expected outcome, the use case is not satisfied
                        if actual_value != expected_value:
                            use_case_satisfied = False
                            break  # No need to check further conditions for this record

                # Append the result for this record
                use_case_results.append(use_case_satisfied)
                self._add_use_case_assessment_result(use_case,row['record_id'], use_case_satisfied)

            # Add the results as a new column to the DataFrame
            df[use_case] = use_case_results

        # Output RTL Result file: Serialize the graph with the results

        self.manager.results_graph.serialize(destination=self.output_result_file, format="turtle")


        return df

    def convert_to_excel(self, output_file_path):
        df = self.parse_turtle()
        df.to_excel(output_file_path, index=False, engine='openpyxl')

    def _add_use_case_assessment_result(self, use_case, record_id, value, assessment_date=None):
        subject=URIRef(f"http://example.com/use_case_assessment/{use_case}/{record_id}")
        assessment_type=URIRef(f"http://example.com/use_case_assessment/{use_case}/")
        result_bn = BNode()
        self.manager.results_graph.add((subject, DQAF.hasDQAFResult, result_bn))
        self.manager.results_graph.add((result_bn, SOSA.observedProperty, assessment_type))

        self.manager.results_graph.add((result_bn, SDO.value, Literal(value)))
        # Check if assessment_date is None, and replace it with date.date.now()
        if assessment_date is None:
            assessment_date = datetime.now()
        elif isinstance(assessment_date, datetime.date) and not isinstance(assessment_date, datetime.datetime):
            assessment_date = datetime.datetime.combine(assessment_date, datetime.time.min)

        self.manager.results_graph.add((result_bn, SOSA.resultTime, Literal(assessment_date, datatype=XSD.dateTime)))
