import pytest
from pyoxigraph import Store

# Import test data generators
from Convert.test_data_generation.data_generation_date_recency import create_date_recency_test_data
from Convert.test_data_generation.data_generation_date_completeness import create_date_completeness_test_data
from Convert.test_data_generation.data_generation_date_format_validation import create_date_format_validation_test_data
from Convert.test_data_generation.data_generation_coordinate_completeness import create_coordinate_completeness_test_data
from Convert.test_data_generation.data_generation_coordinate_precision import create_coordinate_precision_test_data
from Convert.test_data_generation.data_generation_geospatial_accuracy_precision import create_geospatial_accuracy_precision_test_data
from Convert.test_data_generation.data_generation_datum_completeness import create_datum_completeness_test_data
from Convert.test_data_generation.data_generation_datum_type import create_datum_type_test_data
from Convert.test_data_generation.data_generation_scientific_name_completeness import create_scientific_name_completeness_test_data
from Convert.test_data_generation.data_generation_scientific_name_validation import create_scientific_name_validation_test_data

# Test many SPARQL rules in one function
@pytest.mark.parametrize("name, data_func, sparql_file, expected", [
    (
        "date_recency",
        create_date_recency_test_data,
        "../queries/assess_date_recency.sparql",
        {
            "https://w3id.org/tern/ontologies/tern/observation1": "recent_20_years",
            "https://w3id.org/tern/ontologies/tern/observation2": "outdated_20_years"
        }
    ),
    (
        "date_completeness",
        create_date_completeness_test_data,
        "../queries/assess_date_completeness.sparql",
        {
            "https://w3id.org/tern/ontologies/tern/obs_with_date": "non_empty",
            "https://w3id.org/tern/ontologies/tern/obs_no_date": "empty",
            "https://w3id.org/tern/ontologies/tern/obs_missing_date": "empty"
        }
    ),
    (
        "date_format_validation",
        create_date_format_validation_test_data,
        "../queries/assess_date_format_validation.sparql",
        {
            "http://example.com/obs/obs_valid": "valid",
            "http://example.com/obs/obs_invalid": "invalid"
        }
    ),
    (
        "coordinate_completeness",
        create_coordinate_completeness_test_data,
        "../queries/assess_coordinate_completeness.sparql",
        {
            "http://example.com/test/obs_with_coords": "non_empty",
            "http://example.com/test/obs_no_coords": "empty",
            "http://example.com/test/obs_missing_wkt": "empty"
        }
    ),
    (
        "coordinate_precision",
        create_coordinate_precision_test_data,
        "../queries/assess_coordinate_precision.sparql",
        {
            "http://example.com/test/obs_high": "High",
            "http://example.com/test/obs_medium": "Medium",
            "http://example.com/test/obs_low": "Low"
        }
    ),
    (
        "geo_spatial_accuracy_precision",
        create_geospatial_accuracy_precision_test_data,
        "../queries/assess_geo_spatial_accuracy_precision.sparql",
        {
            "http://example.com/test/obs_high": "high_precision",
            "http://example.com/test/obs_low": "low_precision",
            "http://example.com/test/obs_missing": "low_precision"
        }
    ),
    (
        "datum_completeness",
        create_datum_completeness_test_data,
        "../queries/assess_datum_completeness.sparql",
        {
            "http://example.com/test/obs_with_datum": "not_empty",
            "http://example.com/test/obs_no_datum": "empty"
        }
    ),
    (
        "datum_type",
        create_datum_type_test_data,
        "../queries/assess_datum_validation.sparql",
        {
            "http://example.com/test/obs_agd84": "AGD84",
            "http://example.com/test/obs_gda94": "GDA94",
            "http://example.com/test/obs_gda2020": "GDA2020",
            "http://example.com/test/obs_wgs84": "WGS84",
            "http://example.com/test/obs_none": "None"
        }
    ),
    (
        "scientific_name_completeness",
        create_scientific_name_completeness_test_data,
        "../queries/assess_scientific_name_completeness.sparql",
        {
            "http://example.com/test/obs_with_name": "non_empty_name",
            "http://example.com/test/obs_no_name": "empty_name"
        }
    ),
    (
        "scientific_name_validation",
        create_scientific_name_validation_test_data,
        "../queries/assess_scientific_name_validation.sparql",
        {
            "http://example.com/test/obs_valid": "valid_name",
            "http://example.com/test/obs_invalid": "valid_name"  # still a placeholder
        }
    )
])
def test_dqaf_dimensions(name, data_func, sparql_file, expected):
    """
    Runs SPARQL file for each DQAF rule.
    Checks if output matches expected results.
    """

    # Load test data into RDF store
    turtle_data = data_func()
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # Load the SPARQL rule
    with open(sparql_file, "r") as f:
        insert_query = f.read()
    store.update(insert_query)

    # Query the output results
    select_query = f"""
    PREFIX dqaf: <http://example.com/def/dqaf/>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX schema: <http://schema.org/>

    SELECT ?observation ?value
    WHERE {{
      GRAPH dqaf:fullResults {{
        ?observation dqaf:hasResult [
          sosa:observedProperty <http://example.com/assess/{name}/> ;
          schema:value ?value
        ] .
      }}
    }}
    """
    results = store.query(select_query)

    # Collect actual values
    actual_results = {
        str(row["observation"]).strip("<>"): row["value"].value
        for row in results
    }

    # Print results for debugging
    print(f"\n=== Extracted Results ({name}) ===")
    for obs, val in actual_results.items():
        print(f"{obs} => {val}")

    # Compare with expected values
    for obs_uri, expected_val in expected.items():
        assert obs_uri in actual_results, f"[{name}] Missing: {obs_uri}"
        assert actual_results[obs_uri] == expected_val, \
            f"[{name}] Expected: {expected_val}, Got: {actual_results[obs_uri]}"
