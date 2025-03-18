# This script test_type1: SPARQL query returns DQ results the `assess_date_recency.py` script to ensure it works correctly.

import subprocess
import pytest


def test_date_recency_script():
    # Run the `assess_date_recency.py` script as a subprocess.
    result = subprocess.run(["python", "../functions/assess_date_recency.py"], capture_output=True, text=True)

    # Capture the script's output and split it into separate lines.
    output_lines = result.stdout.strip().split("\n")

    # Check if the script ran successfully (exit code 0 means no errors).
    assert result.returncode == 0

    # Verify that the expected counts of recent and outdated observations are present in the output.
    assert "Total 'recent_20_years': 404" in output_lines
    assert "Total 'outdated_20_years': 96" in output_lines
