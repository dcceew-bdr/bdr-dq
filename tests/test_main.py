import os
import shutil

import pytest
from rdflib import Graph, URIRef, Literal, SOSA
from rdflib.namespace import SDO
from rdflib.plugins.parsers.notation3 import BadSyntax
# from dq.__main__ import load_data, assessment_01
from dq.__main__ import main
from pathlib import Path

from dq.assess import RDFDataQualityAssessment
from dq.defined_namespaces import DirectoryStructure


def test_version_information(monkeypatch, capsys):
    # Simulate command-line arguments
    args = ["dq", "--version"]
    monkeypatch.setattr('sys.argv', args)

    # Call the main function (which no longer is expected to raise SystemExit)
    main()

    # Verify that version information is printed
    captured = capsys.readouterr()
    assert "0.0.1" in captured.out


def test_data_to_assess_input(monkeypatch, capsys):
    # Simulate command-line arguments including the path to your test RDF file
    file_to_assess = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')

    args = ["dq", "--data-to-assess", str(file_to_assess)]
    monkeypatch.setattr('sys.argv', args)

    # Call the main function
    main()

    # Capture the standard output and error
    captured = capsys.readouterr()

    # Assert that the final output is as expected
    assert "Complete" in captured.out


def test_output_files_creation(monkeypatch, tmp_path):
    # Define the source Turtle file and the template input file paths
    source_turtle_file = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')
    template_input_file = tmp_path / "data" / "chunk_1.ttl"  # Example path

    # Ensure the target directory exists
    template_input_file.parent.mkdir(parents=True, exist_ok=True)

    # Copy the source Turtle file to the template input file
    shutil.copy(source_turtle_file, template_input_file)

    # Now, simulate command-line arguments with the copied file as input

    args = ["dq", "--data-to-assess", str(template_input_file)]
    monkeypatch.setattr('sys.argv', args)

    # Call the main function
    main()

    file_base_path = DirectoryStructure()

    expected_files = [
        os.path.join(file_base_path.report_base_path, "Report.txt"),
        os.path.join(file_base_path.result_base_path, "Final_Usecase_Results.ttl"),
        os.path.join(file_base_path.template_base_path, 'usecase_template.xlsx'),
        os.path.join(file_base_path.use_case_base_path, 'usecase_definition.xlsx'),
        os.path.join(file_base_path.result_base_path, 'output.xlsx'),
        os.path.join(file_base_path.result_base_path, "Results.ttl"),

    ]

    # Verify that all expected files have been created
    for file_path in expected_files:
        assert os.path.exists(file_path), f"File {file_path} was not created"


def test_assess_date_recency():
    file_to_assess = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')
    g = Graph().parse(str(file_to_assess))

    # Actual results of the assessment
    total_assessments, result_counts = RDFDataQualityAssessment(g, None).assess_date_recency()

    expected_total_assessments = 100
    expected_recent = 73  # Expected number of recent dates
    expected_outdated = 27  # Expected number of outdated dates

    # Assertions to verify the outcome
    assert total_assessments == expected_total_assessments, f"Expected {expected_total_assessments} assessments, got {total_assessments}"
    assert result_counts[
               'recent'] == expected_recent, f"Expected {expected_recent} recent dates, got {result_counts['recent']}"
    assert result_counts[
               'outdated'] == expected_outdated, f"Expected {expected_outdated} outdated dates, got {result_counts['outdated']}"


def test_assess_point_in_australia_state():
    file_to_assess = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')
    g = Graph().parse(str(file_to_assess))

    # Actual results of the assessment
    total_assessments, result_counts = RDFDataQualityAssessment(g, None).assess_point_in_australia_state()

    expected_total_assessments = 100

    expected_results_counts = {
        "Outside_Australia": 35,
        "Northern_Territory": 11,
        "New_South_Wales": 12,
        "Queensland": 15,
        "Western_Australia": 20,
        "South_Australia": 6,
        "Victoria": 1}

    # Assertions to verify the outcome
    assert total_assessments == expected_total_assessments, f"Expected {expected_total_assessments} assessments, got {total_assessments}"

    for state, expected_count in expected_results_counts.items():
        assert result_counts[
                   state] == expected_count, f"Expected {expected_count} for state {state}, got {result_counts[state]}"
