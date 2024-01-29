import time
from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import SDO, SOSA, XSD
import argparse
import sys
from pathlib import Path
from typing import Union
from dq.defined_namespaces import DQAF

__version__ = "0.0.1"


def load_data(path_or_graph: Union[Path, Graph]) -> Graph:
    if isinstance(path_or_graph, Path):
        return Graph().parse(path_or_graph)
    elif isinstance(path_or_graph, Graph):
        return path_or_graph
    else:
        raise ValueError("Could not load data_to_assess: you must supply either a file or an RDF Graph object")


def assessment_01(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/01")
    result_graph = Graph()
    result_graph.bind("dqaf", DQAF)
    target = URIRef("http://example.com/thingWithResult")
    result_bn = BNode()
    graph_length = len(g)

    if graph_length < 2:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(0)))
    elif 2 < graph_length < 3:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(2)))
    elif graph_length >= 3:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(5)))

    return result_graph


def assessment_medi(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/medi")
    result_graph = Graph()
    result_graph.bind("dqaf", DQAF)

    q1 = """
        PREFIX schema: <https://schema.org/>
        
        SELECT ?person_iri 
        WHERE {
            ?person_iri a schema:Person .
        }
        """

    targets = set()

    for r in g.query(q1):
        targets.add(r[0])

    for target in targets:
        result_bn = BNode()

        q2 = """
            PREFIX schema: <https://schema.org/>
            
            SELECT (COUNT(?name) AS ?count)
            WHERE {
                <xxx> schema:name ?name .
            }
            """.replace("xxx", target)

        no_names = 0
        for r in g.query(q2):
            no_names = int(r[0])

        result_graph.add((URIRef(target), DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))

        if no_names >= 2:
            result_graph.add((result_bn, SDO.value, Literal(True, datatype=XSD.boolean)))
        else:
            result_graph.add((result_bn, SDO.value, Literal(False, datatype=XSD.boolean)))

    return result_graph


def cli(args=None):
    parser = argparse.ArgumentParser(
        prog="dq",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-v",
        "--version",
        help="The version and other info for this instancs of BDR DQ",
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--shacl-validate",
        help="Validate the RDF file with ABIS validation before performing quality assessment",
        action="store_true",
    )

    parser.add_argument(
        "data_to_assess",
        # nargs="?",  # allow 0 or 1 file name as argument
        type=Path,
        help="The ABIS-compliant RDF file, or an RDFLib graph object, to assess",
    )

    return parser.parse_args(args)


def main(args=None):
    if args is None:  # run via entrypoint
        args = cli(sys.argv[1:])

    if args.version:
        print(__version__)
        exit()

    if args.shacl_validate:
        print("Validating input data...")
        # do nothing for now

    # main program
    print("Running BDR-DQ...")
    g = load_data(args.data_to_assess)

    rg = assessment_01(g)
    rg += assessment_medi(g)

    rg.serialize(destination="results.ttl", format="longturtle")
    print("Complete")


if __name__ == "__main__":
    main()
