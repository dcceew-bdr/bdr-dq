import json
import uuid
from datetime import datetime
from pathlib import Path
from pyoxigraph import Store, RdfFormat, NamedNode

from rdflib import URIRef, Graph, Namespace, RDF, DCTERMS, Literal, XSD, SOSA


def run_dqf(turtle_data: str, query_dir: str = "queries"):
    store = Store()
    store.load(turtle_data.encode("utf-8"), format=RdfFormat.TURTLE)

    output_dir = Path(f"output")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open("compression/vocabulary_versions.json") as f:
        vv = json.load(f)
    current_version = vv["current_version"]
    compression_query = Path(f"compression/queries/compress_v{current_version}.rq").read_text()

    # add a run ID to the compression query
    uid = uuid.uuid4().hex
    run_uri = URIRef(f"https://bdr-dqf-compression/run-id/{uid}")
    compression_query = compression_query.replace(
        "VALUES ?run_id { UNDEF }",
        f"VALUES ?run_id { {uid} }",
    )

    # create RDF details for the run
    g = Graph()
    BDRDQF = Namespace("https://bdr-dqf-compression/")
    g.bind("bdrdqf", BDRDQF)
    g.add((run_uri, RDF.type, BDRDQF["AssessmentRun"]))
    g.add((run_uri, DCTERMS.identifier, Literal(uid)))
    now_literal = Literal(datetime.now().isoformat(), datatype=XSD.dateTime)
    g.add((run_uri, SOSA.resultTime, now_literal))
    g.add((run_uri, BDRDQF.usedCompressionVersion, Literal(current_version)))
    g.serialize(output_dir/f"{uid}-metadata.ttl", format="turtle")

    query_dir_path = Path(query_dir)
    for query_path in query_dir_path.glob("*.rq"):
        print(f"Running query: {query_path}")
        with query_path.open("r") as file:
            result_generation_query = file.read()
        try:
            store.update(result_generation_query)  # adds the full results to the dataset
        except Exception as e:
            print(f"Error running query {query_path}: {e}")
    # compress all results, adding to the https://linked.data.gov.au/def/bdr/dqaf/compressedResults Graph.
    compressed_results = store.query(compression_query)
    with open(output_dir/f"{uid}.ttl", "wb") as f:
        f.write(compressed_results.serialize(format=RdfFormat.TURTLE))


if __name__ == "__main__":
    turtle = Path("../Old Implementation/SPARQL Codes and Tests/chunk_1 samplae input data for test.ttl").read_text()
    run_dqf(turtle)
