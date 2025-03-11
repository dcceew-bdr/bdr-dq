from rdflib.namespace import DefinedNamespace
from rdflib.namespace import Namespace, URIRef
import os


class DQAF(DefinedNamespace):
    _NS = Namespace("https://linked.data.gov.au/def/bdr/dqaf/")

    Assessment: URIRef
    hasDQAFResult: URIRef
    assessmentDate: URIRef


# Additional namespaces
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")


class DirectoryStructure:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)  # Gets the directory in which this script is located
        self.map_base_path = os.path.join(self.base_path, 'map')  # Path to the 'map' directory
        self.output_base_path = os.path.join(self.base_path, 'output')  # Path to the 'output' directory
        self.result_base_path = os.path.join(self.base_path, 'result')  # Path to the 'result' directory
        self.template_base_path = os.path.join(self.base_path, 'template')  # Path to the 'template' directory
        self.use_case_base_path = os.path.join(self.base_path, 'use_case')  # Path to the 'use_case' directory
        self.report_base_path = os.path.join(self.base_path, 'report')  # Path to the 'report' directory
        self.scoring_base_path = os.path.join(self.base_path, 'score')  # Path to the 'score' directory
        self.input_base_path = os.path.join(self.base_path, 'input')  # Path to the 'input' directory
        self.document_base_path = os.path.join(self.base_path, 'doc')  # Path to the 'doc' directory
