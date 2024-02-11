import time
from rdflib import Graph, URIRef, Literal, Namespace, BNode
from rdflib.namespace import SDO, SOSA, XSD
import argparse
import sys
from pathlib import Path
from typing import Union

from datetime import datetime
from .assess import load_data, assessment_01, assessment_medi, dateWithinLast20Years, check_lat_high_precision
from dq.defined_namespaces import DQAF, GEO, SOSA, TIME

__version__ = "0.0.1"

def cli(args=None):
    parser = argparse.ArgumentParser(
        prog="dq",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-v",
        "--version",
        help="The version and other info for this instances of BDR DQ",
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

    print("Running BDR-DQ...")
    g = load_data(args.data_to_assess)

    rg = dateWithinLast20Years(g)
    rg = check_lat_high_precision(g)
    rg.serialize(destination="results.ttl", format="longturtle")

    print("Complete")

if __name__ == "__main__":
    main()
