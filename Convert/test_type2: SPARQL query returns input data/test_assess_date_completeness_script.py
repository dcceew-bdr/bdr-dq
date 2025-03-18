import subprocess  # Import subprocess to run external scripts
import pytest  # Import pytest for testing

def test_date_completeness_script():
    """
    This function runs the `assess_date_completeness.py` script and checks if it produces the expected output.
    """

    # Run the script `assess_date_completeness.py` as a separate process.
    # `capture_output=True` means we collect the output, and `text=True` ensures the output is in text format.
    result = subprocess.run(["python", "../functions/assess_date_completeness.py"], capture_output=True, text=True)

    # Capture the output of the script and split it into separate lines for processing.
    output_lines = result.stdout.strip().split("\n")

    # Check if the script executed successfully.
    # `returncode == 0` means the script ran without errors.
    assert result.returncode == 0, "Error: The script did not execute successfully."

    # Find the line in the output that mentions the count of 'non_empty' observations.
    summary_line_present = next((line for line in output_lines if "Total 'non_empty':" in line), None)

    # Find the line in the output that mentions the count of 'empty' observations.
    summary_line_missing = next((line for line in output_lines if "Total 'empty':" in line), None)

    # Check if the number of 'non_empty' observations is as expected (500).
    assert summary_line_present == "Total 'non_empty': 500", f"Unexpected output: {summary_line_present}"

    # Check if the number of 'empty' observations is as expected (0).
    assert summary_line_missing == "Total 'empty': 0", f"Unexpected output: {summary_line_missing}"
