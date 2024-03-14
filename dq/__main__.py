import argparse
import sys
from pathlib import Path
import os

# Inside __main__.py


# Assuming RDFDataQualityAssessment is correctly imported from assess.py
from dq.assess import RDFDataQualityAssessment

__version__ = "0.0.1"

from dq.defined_namespaces import DirectoryStructure

from dq.vocab_manager import VocabManager

from dq.query_processor import RDFQueryProcessor
from dq.usecase_manager import UseCaseManager, TurtleToExcelConverter


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
    directory_structure = DirectoryStructure()

    report_txt_file = os.path.join(directory_structure.report_base_path,
                                   'Report.txt')

    with open(report_txt_file, "w") as report_file:
        dq_assessment = RDFDataQualityAssessment(args.data_to_assess, report_file)
        result_filename = os.path.join(dq_assessment.directory_structure.result_base_path, "Results.ttl")

        all_labels = dq_assessment.label_manager.create_excel_template(
            os.path.join(dq_assessment.directory_structure.template_base_path, 'usecase_template.xlsx'))
        print("All Labels:", all_labels)

        # Generate overall report
        dq_assessment.report_analysis.generate_report()

        # Perform assessments
        dq_assessment.assessments()

        # Output RTL Result file: Serialize the graph with the results
        dq_assessment.g.serialize(destination=result_filename, format="turtle")
        use_case_definition_file = os.path.join(dq_assessment.directory_structure.use_case_base_path,
                                                'usecase_definition.xlsx')
        out_put_result_file = os.path.join(dq_assessment.directory_structure.result_base_path,
                                           'Final_Usecase_Results.ttl')
        output_excel_file = os.path.join(dq_assessment.directory_structure.result_base_path,
                                         'output.xlsx')

        # Usage
        converter = TurtleToExcelConverter(result_filename, use_case_definition_file, out_put_result_file)
        converter.convert_to_excel(output_excel_file)

    print("Complete")


if __name__ == "__main__":
    main()
