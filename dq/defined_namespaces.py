from rdflib.namespace import DefinedNamespace
from rdflib.namespace import Namespace, URIRef


class DQAF(DefinedNamespace):
    _NS = Namespace("https://linked.data.gov.au/def/bdr/dqaf/")

    Assessment: URIRef
    hasDQAFResult: URIRef
    assessmentDate: URIRef


# Additional namespaces
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

