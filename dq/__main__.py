import argparse
import sys
from pathlib import Path
# Inside __main__.py


# Assuming RDFDataQualityAssessment is correctly imported from assess.py
from dq.assess import RDFDataQualityAssessment

__version__ = "0.0.1"

from dq.label_manager import LabelManager

from dq.query_processor import RDFQueryProcessor
from dq.usecase_manager import UseCaseManager


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
        help="Validate the RDF file with SHACL validation before performing quality assessment",
        action="store_true",
    )

    parser.add_argument(
        "data_to_assess",
        type=Path,
        help="The ABIS-compliant RDF file, or an RDFLib graph object, to assess",
    )

    return parser.parse_args(args)


def main(args=None):
    if args is None:  # If run via entrypoint
        args = cli(sys.argv[1:])

    if args.version:
        print(__version__)
        return

    if args.shacl_validate:
        print("Validating input data...")
        # Add SHACL validation logic here if necessary

    print("Running BDR-DQ...")
    # Directly pass the data_to_assess to the class, which handles loading
    print(args.data_to_assess)

    result_filename = "Results.ttl"

    with open("Report.txt", "w") as report_file:
        dq_assessment = RDFDataQualityAssessment(args.data_to_assess, report_file)

        all_labels = dq_assessment.label_manager.create_excel_template('usecase_template.xlsx')
        print("All Labels:", all_labels)

        # Generate overall report
        dq_assessment.report_analysis.generate_report()

        # Perform assessments
        dq_assessment.assessments()

        # Output RTL Result file: Serialize the graph with the results
        dq_assessment.g.serialize(destination=result_filename, format="turtle")

        # Example usage of the usecase manager
        excel_file_path = 'usecase_definition.xlsx'
        results_ttl_path = 'Results.ttl'
        output_ttl_file_path = 'Final_Usecase_Results.ttl'

        manager = UseCaseManager(excel_file_path, results_ttl_path)
        manager.read_excel()
        manager.load_rdf_results()
        manager.create_use_case_matrix()
        manager.assess_use_cases()
        manager.write_results_to_ttl(output_ttl_file_path)

    print("Complete")


if __name__ == "__main__":
    main()
