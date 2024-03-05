
from rdflib.namespace import DefinedNamespace
from rdflib.namespace import Namespace, URIRef, SOSA, TIME, GEO, SKOS, XSD, DCTERMS, FOAF, PROV, RDF, RDFS, VOID


class DQAF(DefinedNamespace):
    _NS = Namespace("https://linked.data.gov.au/def/bdr/dqaf/")

    Assessment: URIRef
    hasDQAFResult: URIRef
    assessmentDate: URIRef


# Additional namespaces

BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")

DWC = Namespace("http://rs.tdwg.org/dwc/terms/")

TERN = Namespace("https://w3id.org/tern/ontologies/tern/")


# Define a mapping of namespaces to prefixes
namespace_map = {
    str(BDRM): "bdrm",
    str(DCTERMS): "dcterms",
    str(DWC): "dwc",
    str(FOAF): "foaf",
    str(GEO): "geo",
    str(PROV): "prov",
    str(RDF): "rdf",
    str(RDFS): "rdfs",
    str(SKOS): "skos",
    str(SOSA): "sosa",
    str(TERN): "tern",
    str(TIME): "time",
    str(VOID): "void",
    str(XSD): "xsd"

    # Add more namespace mappings here
}


def uri_to_prefix(uri):
    """Convert a URI to a prefixed name based on known namespaces."""
    for ns, prefix in namespace_map.items():
        if uri.startswith(ns):
            return uri.replace(ns, prefix + ":")
    return uri  # Return the full URI if no prefix mapping is found


def uri_to_prefixed_name(graph, uri):
    """
    Converts a URI to a prefixed name using the graph's registered namespaces.

    Parameters:
    - graph: An RDFLib Graph instance.
    - uri: The URI to convert to a prefixed name.

    Returns:
    - A string representing the prefixed name or the original URI if no prefix is found.
    """
    for prefix, namespace in graph.namespaces():
        if uri.startswith(namespace):
            local_part = uri[len(namespace):]
            return f"{prefix}:{local_part}"
    return uri  # Return the full URI if no matching namespace is found


def bind_namespaces(graph):
    """Bind standard and custom namespaces to the given RDFLib graph."""
    # Standard namespaces already defined in the file
    graph.bind("dcterms", DCTERMS)
    graph.bind("foaf", FOAF)
    graph.bind("geo", GEO)
    graph.bind("prov", PROV)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)
    graph.bind("sosa", SOSA)
    graph.bind("xsd", XSD)
    graph.bind("tern", TERN)
    graph.bind("time", TIME)
    graph.bind("void", VOID)


