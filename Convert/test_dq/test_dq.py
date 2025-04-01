import pytest
from pyoxigraph import Store

# Import test data generation functions
from Convert.test_data_generation.data_generation_date_recency import create_date_recency_test_data
from Convert.test_data_generation.data_generation_date_completeness import create_date_completeness_test_data
from Convert.test_data_generation.data_generation_date_format_validation import create_date_format_validation_test_data
from Convert.test_data_generation.data_generation_coordinate_completeness import create_coordinate_completeness_test_data
from Convert.test_data_generation.data_generation_coordinate_precision import create_coordinate_precision_test_data
from Convert.test_data_generation.data_generation_geospatial_accuracy_precision import create_geospatial_accuracy_precision_test_data
from Convert.test_data_generation.data_generation_datum_completeness import create_datum_completeness_test_data

# Parametrized test cases
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
    )
])
def test_dqaf_dimensions(name, data_func, sparql_file, expected):
    """
    Generalized test for DQAF assessments using pytest parametrization.
    """

    # === Step 1: Generate RDF test data ===
    turtle_data = data_func()
    store = Store()
    store.load(turtle_data.encode("utf-8"), format="text/turtle")

    # === Step 2: Run SPARQL INSERT query ===
    with open(sparql_file, "r") as f:
        insert_query = f.read()
    store.update(insert_query)

    # === Step 3: Query inserted values from dqaf:fullResults ===
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
        ]
      }}
    }}
    """
    results = store.query(select_query)

    # === Step 4: Convert result to dictionary ===
    actual_results = {
        str(row["observation"]).strip("<>"): row["value"].value
        for row in results
    }

    print(f"\nExtracted Results ({name}):", actual_results)

    # === Step 5: Assert expected results match actual ones ===
    for obs_uri, expected_val in expected.items():
        assert obs_uri in actual_results, f"[{name}] Missing: {obs_uri}"
        assert actual_results[obs_uri] == expected_val, \
            f"[{name}] Expected: {expected_val}, Got: {actual_results[obs_uri]}"
