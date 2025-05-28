def generate_full_dqaf_test_data():
    """
    Make simple test data for 3 observations:
    - obs1: mostly good results → FFP1
    - obs2: mix of good and bad → FFP2
    - obs3: many bad results → FFP3
    """
    data = []

    # ====================
    # obs1 → High quality (FFP1)
    # All results are good
    # ====================
    data.extend([
        ("obs1", "coordinate_precision", "High"),
        ("obs1", "coordinate_completeness", "non_empty"),
        ("obs1", "coordinate_outlier_irq", "normal_coordinate"),
        ("obs1", "coordinate_outlier_zscore", "normal_coordinate"),
        ("obs1", "coordinate_unusual", "normal_coordinate"),
        ("obs1", "coordinate_in_australia_state", "in_australia"),
        ("obs1", "date_completeness", "non_empty"),
        ("obs1", "date_format_validation", "valid"),
        ("obs1", "date_outlier_irq", "normal_date"),
        ("obs1", "date_outlier_kmeans", "normal_date"),
        ("obs1", "date_recency", "recent_20_years"),
        ("obs1", "datum_completeness", "not_empty"),
        ("obs1", "datum_type", "WGS84"),
        ("obs1", "datum_validation", "valid"),
        ("obs1", "scientific_name_completeness", "non_empty_name"),
        ("obs1", "scientific_name_validation", "valid_name"),
    ])

    # ====================
    # obs2 → Medium quality (FFP2)
    # Some bad, some good
    # ====================
    data.extend([
        ("obs2", "coordinate_precision", "High"),
        ("obs2", "coordinate_completeness", "empty"),
        ("obs2", "coordinate_outlier_irq", "normal_coordinate"),
        ("obs2", "coordinate_outlier_zscore", "outlier_coordinate"),
        ("obs2", "coordinate_unusual", "unusual_coordinate"),
        ("obs2", "coordinate_in_australia_state", "in_australia"),
        ("obs2", "date_completeness", "non_empty"),
        ("obs2", "date_format_validation", "valid"),
        ("obs2", "date_outlier_irq", "outlier_date"),
        ("obs2", "date_outlier_kmeans", "normal_date"),
        ("obs2", "date_recency", "outdated_20_years"),
        ("obs2", "datum_completeness", "not_empty"),
        ("obs2", "datum_type", "GDA94"),
        ("obs2", "datum_validation", "invalid"),
        ("obs2", "scientific_name_completeness", "empty_name"),
        ("obs2", "scientific_name_validation", "valid_name"),
    ])

    # ====================
    # obs3 → Low quality (FFP3)
    # Most results are bad
    # ====================
    data.extend([
        ("obs3", "coordinate_precision", "Low"),
        ("obs3", "coordinate_completeness", "empty"),
        ("obs3", "coordinate_outlier_irq", "outlier_coordinate"),
        ("obs3", "coordinate_outlier_zscore", "outlier_coordinate"),
        ("obs3", "coordinate_unusual", "unusual_coordinate"),
        ("obs3", "coordinate_in_australia_state", "outside_australia"),
        ("obs3", "date_completeness", "empty"),
        ("obs3", "date_format_validation", "invalid"),
        ("obs3", "date_outlier_irq", "outlier_date"),
        ("obs3", "date_outlier_kmeans", "outlier_date"),
        ("obs3", "date_recency", "outdated_20_years"),
        ("obs3", "datum_completeness", "empty"),
        ("obs3", "datum_type", "None"),
        ("obs3", "datum_validation", "invalid"),
        ("obs3", "scientific_name_completeness", "empty_name"),
        ("obs3", "scientific_name_validation", "invalid_name"),
    ])

    return data
