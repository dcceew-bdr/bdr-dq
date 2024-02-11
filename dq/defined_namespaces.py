from rdflib import Namespace, URIRef
from rdflib.namespace import DefinedNamespace

class DQAF(DefinedNamespace):
    _NS = Namespace("https://linked.data.gov.au/def/bdr/dqaf/")

    Assessment: URIRef
    hasDQAFResult: URIRef
    assessmentDate: URIRef

# Additional namespaces
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
