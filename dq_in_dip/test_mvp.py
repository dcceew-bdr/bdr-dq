import json
from io import StringIO

import numpy as np
import pandas as pd
from pyoxigraph import QueryResultsFormat
from rdflib import URIRef, Literal, XSD
from shapely.wkt import loads

from conftest import QUERY_DIR
from dq_in_dip.conftest import add_assessment_result


def test_001(store, vocab_manager, result_graph):
    # TODO having now written test_002, this test_001 could actually reuse the get_observation_geometries fixture as
    #  well, rather than needing to run a separate query. The last step of the analysis would then be outside the SPARQL
    #  query.
    """
    coordinate_completeness
    This is an example of an assessment that can be done in SPARQL.
    """
    assessment_name = "coordinate_completeness"
    namespace, assess_namespace, result_counts, total_assessments = vocab_manager.init_assessment(
        assessment_name)

    query = (QUERY_DIR/"001.rq").read_text()
    results_json = store.query(query).serialize(format=QueryResultsFormat.JSON)
    results_dict = json.loads(results_json)
    for result in results_dict["results"]["bindings"]:
        observation = URIRef(result["observation"]["value"])
        hasNonEmptyPoint = result["hasNonEmptyPoint"]["value"]
        add_assessment_result(result_graph, observation, assess_namespace, namespace[hasNonEmptyPoint])

def test_002(vocab_manager, result_graph, get_observation_geometries):
    """
    coordinate_outlier_irq
    This is an example of an assessment that should be done in Python (statistical analysis), but where the inputs to
    the analysis can come from a SPARQL query.
    """
    assessment_name = "coordinate_outlier_irq"
    namespace, assess_namespace, result_counts, total_assessments = vocab_manager.init_assessment(
        assessment_name)


    df = pd.read_csv(StringIO(get_observation_geometries))
    df = df[(df['lon'] != 0) | (df['lat'] != 0)]
    df = df.dropna(subset=['lon', 'lat'])

    if df.shape[0] < 4:
        print("Insufficient data for outlier analysis.")
        df['outlier'] = None  # No analysis possible
        return df

    # Compute IQR for latitude and longitude
    lat_q1, lat_q3 = np.percentile(df['lat'], [25, 75])
    long_q1, long_q3 = np.percentile(df['lon'], [25, 75])
    lat_iqr = lat_q3 - lat_q1
    long_iqr = long_q3 - long_q1

    # Identify outliers
    df['lat_outlier'] = (df['lat'] < lat_q1 - 1.5 * lat_iqr) | (df['lat'] > lat_q3 + 1.5 * lat_iqr)
    df['long_outlier'] = (df['lon'] < long_q1 - 1.5 * long_iqr) | (df['lon'] > long_q3 + 1.5 * long_iqr)
    df['outlier'] = df['lat_outlier'] | df['long_outlier']

    outlier_label_map = {
        True: "outlier_coordinate",
        False: "normal_coordinate"
    }

    for result in df.iterrows():
        observation = URIRef(result[1]['observation'])
        outlier = outlier_label_map[result[1]['outlier']]
        add_assessment_result(result_graph, observation, assess_namespace, namespace[outlier])
