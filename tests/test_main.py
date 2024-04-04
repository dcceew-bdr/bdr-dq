import os
import shutil

from rdflib import Graph

from dq.__main__ import main
from dq.assess import RDFDataQualityAssessment
from dq.defined_namespaces import DirectoryStructure
import pytest


@pytest.fixture
def dq_assessment():
    file_to_assess = os.path.join(os.path.dirname(__file__), 'data',
                                  'chunk_1.ttl')
    g = Graph().parse(str(file_to_assess))
    assessment = RDFDataQualityAssessment(g, None)
    return assessment


def test_version_information(monkeypatch, capsys):
    args = ["dq", "--version"]
    monkeypatch.setattr('sys.argv', args)
    main()
    captured = capsys.readouterr()
    assert "0.0.1" in captured.out


def test_data_to_assess_input(monkeypatch, capsys):
    file_to_assess = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')

    args = ["dq", "--data-to-assess", str(file_to_assess)]
    monkeypatch.setattr('sys.argv', args)
    main()
    captured = capsys.readouterr()

    assert "Complete" in captured.out


def test_output_files_creation(monkeypatch, tmp_path):
    source_turtle_file = os.path.join(os.path.dirname(__file__), 'data\chunk_1.ttl')
    template_input_file = tmp_path / "data" / "chunk_1.ttl"  # Example path
    template_input_file.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(source_turtle_file, template_input_file)
    args = ["dq", "--data-to-assess", str(template_input_file)]
    monkeypatch.setattr('sys.argv', args)

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

    for file_path in expected_files:
        assert os.path.exists(file_path), f"File {file_path} was not created"


def do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values):
    assert total_assessments == expected_total_assessments, f"Expected {expected_total_assessments} assessments in {assessment_name}, got {total_assessments}"
    for lbl in expected_label_values:
        assert result_counts[lbl] == expected_label_values[
            lbl], f"Expected {expected_label_values[lbl]} in {assessment_name}, got {result_counts[lbl]}"


def test_assess_date_completeness(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_date_completeness()

    expected_total_assessments = 100
    expected_label_values = {'empty': 0,
                             'non_empty': 100}
    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_date_recency(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_date_recency()

    expected_total_assessments = 100
    expected_label_values = {'recent_20_years': 72,
                             'outdated_20_years': 28}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_datum_completeness(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_datum_completeness()

    expected_total_assessments = 100
    expected_label_values = {'empty': 0,
                             'not_empty': 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_datum_validation(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_datum_validation()

    expected_total_assessments = 100
    expected_label_values = {'valid': 100,
                             'invalid': 0}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_datum_type(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_datum_type()

    expected_total_assessments = 100
    expected_label_values = {'AGD84': 0,
                             'GDA2020': 0,
                             'GDA94': 100,
                             'WGS84': 0,
                             'None': 0}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_precision(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_precision()

    expected_total_assessments = 100
    expected_label_values = {'Low': 38,
                             'Medium': 53,
                             'High': 9}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_completeness(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_completeness()

    expected_total_assessments = 100
    expected_label_values = {'empty': 0,
                             'non_empty': 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_date_outlier_irq(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_date_outlier_irq()

    expected_total_assessments = 100
    expected_label_values = {'outlier_date': 0,
                             'normal_date': 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_date_outlier_kmeans(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_date_outlier_kmeans()

    expected_total_assessments = 100
    expected_label_values = {'outlier_date': 12,
                             'normal_date': 88}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_in_australia_state(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_in_australia_state()

    expected_total_assessments = 100
    expected_label_values = {
        "Outside_Australia": 35,
        "Northern_Territory": 11,
        "New_South_Wales": 12,
        "Queensland": 15,
        "Western_Australia": 20,
        "South_Australia": 6,
        "Victoria": 1}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_date_format_validation(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_date_format_validation()

    expected_total_assessments = 100
    expected_label_values = {
        "valid": 100,
        "invalid": 0}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_unusual(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_unusual()

    expected_total_assessments = 100
    expected_label_values = {
        "usual": 68,
        "unusual": 32}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_outlier_zscore(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_outlier_zscore()

    expected_total_assessments = 100
    expected_label_values = {
        "outlier_coordinate": 0,
        "normal_coordinate": 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_coordinate_outlier_irq(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_coordinate_outlier_irq()

    expected_total_assessments = 100
    expected_label_values = {
        "outlier_coordinate": 0,
        "normal_coordinate": 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_scientific_name_completeness(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_scientific_name_completeness()

    expected_total_assessments = 100
    expected_label_values = {
        "empty_name": 0,
        "non_empty_name": 100}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)


def test_assess_scientific_name_validation(dq_assessment):
    assessment_name, total_assessments, result_counts = dq_assessment.assess_scientific_name_validation()

    expected_total_assessments = 100
    expected_label_values = {
        "valid_name": 100,
        "invalid_name": 0}

    do_the_test(assessment_name, total_assessments, expected_total_assessments, result_counts, expected_label_values)

