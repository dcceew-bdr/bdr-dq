import argparse
import os
import sys
from pathlib import Path
from rdflib import Graph

from dq.assess import RDFDataQualityAssessment
from dq.defined_namespaces import DirectoryStructure
from dq.scoring_manager import ScoringManager
from dq.usecase_manager import UseCaseManager

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
        help="Validate the RDF file with SHACL validation before performing quality assessment",
        action="store_true",
    )

    parser.add_argument(
        "--data-to-assess",
        type=Path,
        help="The ABIS-compliant RDF file, or an RDFLib graph object, to assess",
        required=False  # Make this argument optional
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

    if not hasattr(args, 'data_to_assess') or args.data_to_assess is None:
        print("No data provided to assess.")
        return

    print("Running BDR-DQ...")

    directory_structure = DirectoryStructure()

    report_txt_file = os.path.join(directory_structure.report_base_path,
                                   'Report.txt')
    input_data_to_assess = args.data_to_assess
    is_chunk = True
    if is_chunk:
        # new function
        combined_graph = Graph()

        # Load each TTL file into separate RDF graphs and merge them
        ttl_files = ['chunk_1.ttl', 'chunk_2.ttl', 'chunk_3.ttl', 'chunk_4.ttl']
        print('Combining the chunk files...')
        for ttl_file in ttl_files:
            graph = Graph()
            ttl_file_path = os.path.join(directory_structure.input_base_path, ttl_file)
            print(ttl_file_path)
            graph.parse(ttl_file_path, format='ttl')
            combined_graph += graph

        # Save the combined graph into a TTL file
        combined_ttl_file_path = os.path.join(directory_structure.input_base_path, 'combined_graph.ttl')
        combined_graph.serialize(destination=combined_ttl_file_path, format='turtle')

        combined_graph = Graph()
        combined_graph.parse(combined_ttl_file_path, format='turtle')

        input_data_to_assess = combined_graph

    print(input_data_to_assess)

    with open(report_txt_file, "w") as report_file:
        dq_assessment = RDFDataQualityAssessment(input_data_to_assess, report_file)
        result_filename = os.path.join(dq_assessment.directory_structure.result_base_path, "Results.ttl")

        all_labels = dq_assessment.vocab_manager.create_excel_template(
            os.path.join(dq_assessment.directory_structure.template_base_path, 'usecase_template.xlsx'))
        print("All Labels:", all_labels)

        dq_assessment.report_analysis.generate_report()

        dq_assessment.assessments()

        dq_assessment.g.serialize(destination=result_filename, format="turtle")
        use_case_definition_file = os.path.join(dq_assessment.directory_structure.use_case_base_path,
                                                'usecase_definition.xlsx')
        scoring_definition_file = os.path.join(dq_assessment.directory_structure.scoring_base_path,
                                               'assertions_score_weighting_definition.xlsx')
        output_result_file = os.path.join(dq_assessment.directory_structure.result_base_path,
                                          'Final_Usecase_Results.ttl')
        dq_assessment.result_matrix_df = dq_assessment.result_matrix_df.sort_values(by='observation_id', ascending=True)
        dq_assessment.result_matrix_df.to_excel(os.path.join(dq_assessment.directory_structure.result_base_path,
                                                             'output1.xlsx'), sheet_name="matrix", index=None)

        use_case_manager = UseCaseManager(use_case_definition_file, dq_assessment.result_matrix_df, result_filename,
                                          output_result_file, report_file)
        use_case_manager.assess_use_cases()
        use_case_manager.result_matrix_df.to_excel(os.path.join(dq_assessment.directory_structure.result_base_path,
                                                                'output2.xlsx'), sheet_name="matrix", index=None)
        scoring_manager = ScoringManager(scoring_definition_file, dq_assessment.result_matrix_df, output_result_file,
                                         output_result_file, report_file)
        scoring_manager.apply_scoring_methods()
        scoring_manager.result_matrix_df.to_excel(os.path.join(dq_assessment.directory_structure.result_base_path,
                                                               'output3.xlsx'), sheet_name="matrix", index=None)

    print("Complete")


if __name__ == "__main__":
    main()
