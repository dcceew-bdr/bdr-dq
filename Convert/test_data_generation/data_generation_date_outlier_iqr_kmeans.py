from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime, timedelta
import random

# Use example namespaces
EX = Namespace("http://example.com/test/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")

def create_date_outlier_iqr_test_data():
    """
    Make test data for checking outlier dates.
    - Some dates are normal (around a base date)
    - Some are outliers (very far in past or future)
    Returns RDF data in Turtle format.
    """

    g = Graph()

    # This is the main date we build others around
    base_date = datetime(2022, 1, 1)

    # 100 normal dates: between -60 to +60 days from base
    for i in range(100):
        delta = timedelta(days=random.randint(-60, 60))
        date = base_date + delta
        add_date_obs(g, i, date)

    # 3 outlier dates: very far from base
    outlier_dates = [
        datetime(2015, 1, 1),  # Past
        datetime(2030, 1, 1),  # Future
        datetime(1990, 1, 1)   # Very old
    ]
    for i, date in enumerate(outlier_dates, start=100):
        add_date_obs(g, i, date)

    return g.serialize(format="turtle")

def add_date_obs(g, i, date):
    """
    This adds one observation with a date to the graph.
    """

    obs = EX[f"obs_{i}"]
    g.add((obs, RDF.type, TERN.Observation))
    g.add((obs, SOSA.resultTime, Literal(date.isoformat(), datatype=XSD.dateTime)))

# If run directly, show part of the result
if __name__ == "__main__":
    ttl_data = create_date_outlier_iqr_test_data()
    print(ttl_data[:1000])
