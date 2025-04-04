import json
import uuid
import argparse
import logging
import sys
from enum import Enum
from datetime import datetime
from pathlib import Path
from pyoxigraph import Store, RdfFormat, NamedNode
from rdflib import URIRef, Graph, Namespace, RDF, DCTERMS, Literal, XSD, SOSA

from compression.generate_compression_query import check_and_generate_compression_files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

# Get the package directory, not the script directory
package_dir = Path(__file__).parent


class AssessmentScope(Enum):
    CHUNK = "Chunk"
    DATASET = "Dataset"
    BDR = "BDR"

    def __str__(self):
        return self.value


def run_assessment(input_file_path: str | Path, scope: AssessmentScope, query_dir_name: str = "queries"):
    """
    Run the data quality assessment framework on an input Turtle file.

    Args:
        input_file_path: Path to the input Turtle file (.ttl)
        scope: Scope of the assessment (Chunk, Dataset, BDR)
        query_dir_name: Directory containing the SPARQL queries

    Returns:
        Path to the output file containing the assessment results
    """
    store = Store()
    store.load(path=input_file_path)

    output_dir = package_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    compression_vocab_path = package_dir / "compression/vocabulary_versions.json"
    with open(compression_vocab_path) as f:
        vv = json.load(f)
    current_version = vv["current_version"]
    compression_query_path = package_dir / f"compression/queries/compress_v{current_version}.rq"
    compression_query = compression_query_path.read_text()

    # add a run ID to the compression query
    uid = uuid.uuid4().hex
    run_uri = URIRef(f"https://bdr-dqf-compression/run-id/{uid}")
    compression_query = compression_query.replace(
        "VALUES ?run_id { UNDEF }",
        f"VALUES ?run_id {{ \"{uid}\" }}",
    )

    # create RDF details for the run
    g = Graph()
    BDRDQF = Namespace("https://bdr-dqf-compression/")
    g.bind("bdrdqf", BDRDQF)
    g.add((run_uri, RDF.type, BDRDQF["AssessmentRun"]))
    g.add((run_uri, DCTERMS.identifier, Literal(uid)))
    now_literal = Literal(datetime.now().isoformat(), datatype=XSD.dateTime)
    g.add((run_uri, SOSA.resultTime, now_literal))
    g.add((run_uri, BDRDQF.usedCompressionVersion, BDRDQF[f"version/{current_version}"]))
    g.add((run_uri, BDRDQF.assessmentScope, BDRDQF[f"scope/{scope.value}"]))
    g.serialize(output_dir / f"{uid}-metadata.ttl", format="turtle")

    query_dir_path = package_dir / query_dir_name
    for query_path in query_dir_path.glob("*.rq"):
        logging.info(f"Running assessment: {query_path.stem}")
        with query_path.open("r") as file:
            result_generation_query = file.read()
        try:
            store.update(result_generation_query)  # adds the full results to the dataset
        except Exception as e:
            logging.error(f"Error running assessment in {query_path}: {e}")
    store.update(compression_query)
    output_filename = output_dir / f"{uid}.nq"
    with open(output_filename, "wb") as f:
        f.write(store.dump(format=RdfFormat.N_QUADS))

    return output_filename


def main():
    """Command-line entry point for the dqaf package."""
    # --- Check and generate compression files first ---
    compression_dir = package_dir / "compression"
    check_and_generate_compression_files(compression_dir)
    # --- End compression check ---

    parser = argparse.ArgumentParser(description="Run Data Quality Framework tests on a Turtle file.")
    parser.add_argument("filename", help="Path to the input Turtle file (.ttl)")
    parser.add_argument(
        "--scope",
        required=True,
        type=AssessmentScope,
        choices=list(AssessmentScope),
        help="Specify the scope of the assessment run (Chunk, Dataset, BDR).",
    )
    args = parser.parse_args()

    input_file_path = Path(args.filename)
    if not input_file_path.is_file():
        logging.error(f"Input file not found at {input_file_path}")
        sys.exit(1)

    try:
        output_file = run_assessment(input_file_path, args.scope)
        logging.info(f"Processing complete. Output file generated: {output_file}")
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()