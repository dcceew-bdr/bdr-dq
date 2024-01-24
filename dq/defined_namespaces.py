from rdflib import Namespace, URIRef
from rdflib.namespace import DefinedNamespace


class DQAF(DefinedNamespace):
    _NS = Namespace("https://linked.data.gov.au/def/bdt/dqaf/")

    Assessment: URIRef

    hasDQAFResult: URIRef
