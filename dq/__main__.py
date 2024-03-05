import argparse
import sys
from pathlib import Path
# Inside __main__.py
from dq.data_quality_assessment.geo.geospatial_checks import GeospatialDataQuality

# Assuming RDFDataQualityAssessment is correctly imported from assess.py
from dq.assess import RDFDataQualityAssessment

__version__ = "0.0.1"

from dq.label_manager import LabelManager

from dq.query_processor import RDFQueryProcessor


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

    result_filename="Results.ttl"

    with open("Report.txt", "w") as report_file:
        dq_assessment = RDFDataQualityAssessment(args.data_to_assess, report_file)

        # Generate overall report
        dq_assessment.report_analysis.generate_report()

        # Perform assessments
        dq_assessment.assess()

        # Output RTL Result file: Serialize the graph with the results
        dq_assessment.g.serialize(destination=result_filename, format="turtle")



    print("Complete")



if __name__ == "__main__":
    main()
