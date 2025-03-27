import json
import hashlib
from pathlib import Path

from rdflib import BNode, URIRef, RDF, Graph, Literal, Namespace, DCTERMS


def calculate_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_max_version(versions_data):
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


def create_queries_and_rdf():
    json_file = "assessments_results_vocabulary.json"
    versions_file = "vocabulary_versions.json"

    current_hash = calculate_hash(json_file)

    try:
        with open(versions_file, 'r') as file:
            versions_data = json.load(file)
    except FileNotFoundError:
        versions_data = {"versions": [], "current_version": 0}

    max_version = get_max_version(versions_data)

    hash_exists = False
    if versions_data.get("versions"):
        for version_info in versions_data["versions"]:
            if version_info.get("hash") == current_hash:
                hash_exists = True
                break

    if not hash_exists:
        new_version = max_version + 1

        versions_data["versions"].append({"version": new_version, "hash": current_hash})
        versions_data["current_version"] = new_version

        with open(versions_file, 'w') as file:
            json.dump(versions_data, file, indent=4)

        with open(json_file, 'r') as file:
            data = json.load(file)
        assessments = [(assessment, i) for i, assessment in  enumerate(data["assessments"], start=1)]
        results = [(result, i) for i, result in enumerate(data["results"], start=1)]

        create_new_query(assessments, results, new_version)
        create_rdf_mapping(assessments, results, new_version)

    else:
        versions_data["current_version"] = next(
            (v["version"] for v in versions_data["versions"] if v["hash"] == current_hash),
            versions_data["current_version"])
        with open(versions_file, 'w') as file:
            json.dump(versions_data, file, indent=4)
        print("Hash already exists, current version updated, no new query file created.")


def create_new_query(assessments, results, new_version):
    assessment_pairs = "\n\t\t\t" + "\n\t\t\t".join(
        [f"( <{uri}> {i} )" for uri, i in assessments])
    result_pairs = "\n\t\t\t" + "\n\t\t\t".join([f"( <{uri}> {i} )" for uri, i in results])
    template_query = Path("queries/_template.rq").read_text()
    populated_query = template_query.replace(
        "VALUES (?assessment ?abbrev_assessment) { ( UNDEF UNDEF ) }",
        "VALUES (?assessment ?abbrev_assessment) {" + assessment_pairs + "}"
    ).replace(
        "VALUES (?result ?abbrev_result) { ( UNDEF UNDEF ) }",
        "VALUES (?result ?abbrev_result) {" + result_pairs + "}"
    ).replace(
        "VALUES ?version { UNDEF }",
        f"VALUES ?version { {new_version} }"
    )
    output_query_file = f"queries/compress_v{new_version}.rq"
    Path("queries").mkdir(parents=True, exist_ok=True)
    with open(output_query_file, 'w') as file:
        file.write(populated_query)
    print(f"Created new query file: {output_query_file}")


def create_rdf_mapping(assessments, results, new_version):
    g = Graph()
    g.bind("dqfcomp", Namespace("https://bdr-dqf-compression/") )
    version_uri = URIRef(f"https://bdr-dqf-compression/v{new_version}")
    has_mapping = URIRef("https://bdr-dqf-compression/hasMapping")
    has_full_uri = URIRef("https://bdr-dqf-compression/hasFullURI")
    has_compressed_literal = URIRef("https://bdr-dqf-compression/hasCompressedLiteral")
    g.add((version_uri, RDF.type, URIRef("https://bdr-dqf-compression/Version")))
    g.add((version_uri, DCTERMS.identifier, Literal(new_version)))
    for assessment in assessments:
        mapping_bnode = BNode()
        g.add((version_uri, has_mapping, mapping_bnode))
        g.add((mapping_bnode, RDF.type, URIRef("https://bdr-dqf-compression/AssessmentMapping")))
        g.add((mapping_bnode, has_full_uri, URIRef(assessment[0])))
        g.add((mapping_bnode, has_compressed_literal, Literal(assessment[1])))
    for result in results:
        result_bnode = BNode()
        g.add((version_uri, has_mapping, result_bnode))
        g.add((result_bnode, RDF.type, URIRef("https://bdr-dqf-compression/ResultMapping")))
        g.add((result_bnode, has_full_uri, URIRef(result[0])))
        g.add((result_bnode, has_compressed_literal, Literal(result[1])))
    g.serialize(f"rdf_mapping/compression_mapping_v{new_version}.ttl",format="turtle")
    print("")

if __name__ == "__main__":
    create_queries_and_rdf()