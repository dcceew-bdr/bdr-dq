import subprocess
import pytest

def test_date_recency_script():
    result = subprocess.run(["python", "assess_date_recency.py"], capture_output=True, text=True)
    output_lines = result.stdout.strip().split("\n")

    assert result.returncode == 0
    assert "Total 'recent_20_years': 404" in output_lines
    assert "Total 'outdated_20_years': 96" in output_lines
