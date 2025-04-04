import json
import hashlib
import logging
from pathlib import Path

from rdflib import BNode, URIRef, RDF, Graph, Literal, Namespace, DCTERMS

log = logging.getLogger(__name__)


def calculate_hash(file_path: Path) -> str:
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_max_version(versions_data: dict) -> int:
    """Gets the maximum version number from the versions data."""
    if not versions_data or not versions_data.get("versions"):
        return 0

    versions = versions_data["versions"]
    if not versions:
        return 0

    max_version = 0
    for version_info in versions:
        version = int(version_info.get("version", 0))
        max_version = max(max_version, version)
    return max_version


def check_and_generate_compression_files(base_dir: Path):
    """
    Checks if the compression vocabulary has changed and generates new
    query and mapping files if necessary. Updates the current version.
    """
    json_vocab_file = base_dir / "assessments_results_vocabulary.json"
    versions_file = base_dir / "vocabulary_versions.json"
    queries_dir = base_dir / "queries"
    rdf_mapping_dir = base_dir / "rdf_mapping"

    if not json_vocab_file.exists():
        log.error(f"Vocabulary file not found: {json_vocab_file}")
        return

    current_hash = calculate_hash(json_vocab_file)

    try:
        with open(versions_file, 'r') as file:
            try:
                versions_data = json.load(file)
            except json.JSONDecodeError:
                log.error(f"Error decoding JSON from {versions_file}. Initializing.")
                versions_data = {"versions": [], "current_version": 0}
    except FileNotFoundError:
        log.info(f"Versions file not found ({versions_file}). Initializing.")
        versions_data = {"versions": [], "current_version": 0}

    max_version = get_max_version(versions_data)

    hash_exists = False
    if versions_data.get("versions"):
        for version_info in versions_data["versions"]:
            # Ensure version is treated as int for comparison if present
            if version_info.get("hash") == current_hash and isinstance(version_info.get("version"), int):
                hash_exists = True
                existing_version = version_info["version"]
                break

    if not hash_exists:
        new_version = max_version + 1
        log.info(f"DQF Vocabulary has changed. Generating new mapping version {new_version}.")

        versions_data["versions"].append({"version": new_version, "hash": current_hash})
        versions_data["current_version"] = new_version

        with open(versions_file, 'w') as file:
            json.dump(versions_data, file, indent=4)

        try:
            with open(json_vocab_file, 'r') as file:
                data = json.load(file)
            assessments = [(assessment, i) for i, assessment in enumerate(data.get("assessments", []), start=1)]
            results = [(result, i) for i, result in enumerate(data.get("results", []), start=1)]

            create_new_query(base_dir, assessments, results, new_version)
            create_rdf_mapping(base_dir, assessments, results, new_version)
        except Exception as e:
            log.error(f"Error processing Vocabulary or creating files: {e}")

    else:
        # Hash exists, check if current_version in the file is consistent
        log.info(f"Vocabulary hash {current_hash} already exists for version {existing_version}.")
        if versions_data.get("current_version") != existing_version:
            log.warning(f"Versions file inconsistency: current_version was {versions_data.get('current_version')}, but hash matches version {existing_version}. Correcting.")
            versions_data["current_version"] = existing_version
            try:
                with open(versions_file, 'w') as file:
                    json.dump(versions_data, file, indent=4)
            except IOError as e:
                log.error(f"Failed to write corrected versions file {versions_file}: {e}")
        else:
            log.info("DQF Vocabulary has not been updated since last run, so continuing with previously generated mapping.")


def create_new_query(base_dir: Path, assessments: list, results: list, new_version: int):
    """Creates a new .rq query file based on the vocabulary."""
    queries_dir = base_dir / "queries"
    template_query_path = queries_dir / "_template.rq"
    output_query_file = queries_dir / f"compress_v{new_version}.rq"

    if not template_query_path.exists():
        log.error(f"Template query file not found: {template_query_path}")
        return

    assessment_pairs = "\n\t\t\t" + "\n\t\t\t".join([f"( <{uri}> {i} )" for uri, i in assessments]) if assessments else ""
    result_pairs = "\n\t\t\t" + "\n\t\t\t".join([f"( <{uri}> {i} )" for uri, i in results]) if results else ""
    template_query = template_query_path.read_text()
    populated_query = template_query.replace(
        "VALUES (?assessment ?abbrev_assessment) { ( UNDEF UNDEF ) }", f"VALUES (?assessment ?abbrev_assessment) {{ {assessment_pairs} }}"
    ).replace(
        "VALUES (?result ?abbrev_result) { ( UNDEF UNDEF ) }", f"VALUES (?result ?abbrev_result) {{ {result_pairs} }}"
    ).replace(
        "VALUES ?version { UNDEF }", f"VALUES ?version {{ {new_version} }}"
    )

    queries_dir.mkdir(parents=True, exist_ok=True)
    with open(output_query_file, 'w') as file:
        file.write(populated_query)
    log.info(f"Created new query file: {output_query_file}")


def create_rdf_mapping(base_dir: Path, assessments: list, results: list, new_version: int):
    """Creates a new .ttl mapping file based on the vocabulary."""
    rdf_mapping_dir = base_dir / "../output"
    output_mapping_file = rdf_mapping_dir / f"compression_mapping_v{new_version}.ttl"

    g = Graph()
    dqfcomp_ns = Namespace("https://bdr-dqf-compression/")
    g.bind("dqfcomp", dqfcomp_ns)
    version_uri = dqfcomp_ns[f"version/{new_version}"]
    has_mapping = dqfcomp_ns["hasMapping"]
    has_full_uri = dqfcomp_ns["hasFullURI"]
    has_compressed_literal = dqfcomp_ns["hasCompressedLiteral"]
    assessment_mapping_type = dqfcomp_ns["AssessmentMapping"]
    result_mapping_type = dqfcomp_ns["ResultMapping"]
    version_type = dqfcomp_ns["Version"]

    g.add((version_uri, RDF.type, version_type))
    g.add((version_uri, DCTERMS.identifier, Literal(new_version)))

    for assessment_uri, assessment_id in assessments:
        mapping_bnode = BNode()
        g.add((version_uri, has_mapping, mapping_bnode))
        g.add((mapping_bnode, RDF.type, assessment_mapping_type))
        g.add((mapping_bnode, has_full_uri, URIRef(assessment_uri)))
        g.add((mapping_bnode, has_compressed_literal, Literal(assessment_id)))

    for result_uri, result_id in results:
        result_bnode = BNode()
        g.add((version_uri, has_mapping, result_bnode))
        g.add((result_bnode, RDF.type, result_mapping_type))
        g.add((result_bnode, has_full_uri, URIRef(result_uri)))
        g.add((result_bnode, has_compressed_literal, Literal(result_id)))

    rdf_mapping_dir.mkdir(parents=True, exist_ok=True)
    g.serialize(output_mapping_file, format="turtle")
    log.info(f"Created RDF mapping file: {output_mapping_file}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    script_dir = Path(__file__).parent
    check_and_generate_compression_files(script_dir)
