from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import SDO, XSD
from datetime import datetime
from typing import Union
from pathlib import Path
import argparse
import sys
from dq.defined_namespaces import DQAF, GEO, SOSA, TIME


def load_data(path_or_graph: Union[Path, Graph]) -> Graph:
    if isinstance(path_or_graph, Path):
        return Graph().parse(path_or_graph)
    elif isinstance(path_or_graph, Graph):
        return path_or_graph
    else:
        raise ValueError("Could not load data_to_assess: you must supply either a file or an RDF Graph object")

def assessment_01(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/01")
    result_graph = Graph()
    result_graph.bind("dqaf", DQAF)
    target = URIRef("http://example.com/thingWithResult")
    result_bn = BNode()
    graph_length = len(g)

    if graph_length < 2:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(0)))
    elif 2 < graph_length < 3:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(2)))
    elif graph_length >= 3:
        result_graph.add((target, DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))
        result_graph.add((result_bn, SDO.value, Literal(5)))

    return result_graph


def assessment_medi(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/medi")
    result_graph = Graph()
    result_graph.bind("dqaf", DQAF)

    q1 = """
            PREFIX schema: <https://schema.org/>

            SELECT ?person_iri 
            WHERE {
                ?person_iri a schema:Person .
            }
            """

    targets = set()

    for r in g.query(q1):
        targets.add(r[0])

    for target in targets:
        result_bn = BNode()

        q2 = """
                PREFIX schema: <https://schema.org/>

                SELECT (COUNT(?name) AS ?count)
                WHERE {
                    <xxx> schema:name ?name .
                }
                """.replace("xxx", target)

        no_names = 0
        for r in g.query(q2):
            no_names = int(r[0])

        result_graph.add((URIRef(target), DQAF.hasDQAFResult, result_bn))
        result_graph.add((result_bn, SOSA.observedProperty, assessment_type))

        if no_names >= 2:
            result_graph.add((result_bn, SDO.value, Literal(True, datatype=XSD.boolean)))
        else:
            result_graph.add((result_bn, SDO.value, Literal(False, datatype=XSD.boolean)))

    return result_graph


def assessObservationDateRecency(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/assessObservationDateRecency")
    assessment_date = datetime.now().date()

    g.bind("dqaf", DQAF)
    g.bind("sosa", SOSA)
    g.bind("xsd", XSD)
    g.bind("time", TIME)

    current_year = assessment_date.year

    for s, p, o in g.triples((None, SOSA.phenomenonTime, None)):
        found_date_within_range = False
        for s2, p2, date in g.triples((o, TIME.inXSDDate, None)):
            if isinstance(date, Literal) and date.datatype == XSD.date:
                year = date.toPython().year
                if (current_year - 20) <= year <= current_year:
                    found_date_within_range = True
                    break

        result_bn = BNode()
        g.add((s, DQAF.hasDQAFResult, result_bn))
        g.add((result_bn, DQAF.assessmentDate, Literal(assessment_date, datatype=XSD.date)))
        g.add((result_bn, SOSA.observedProperty, assessment_type))
        g.add((result_bn, SDO.value, Literal(found_date_within_range, datatype=XSD.boolean)))

    return g


#####################################################
def assess_coordinate_precision1(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/assess_coordinate_precision")
    assessment_date = datetime.now().date()

    g.bind("dqaf", DQAF)
    g.bind("sosa", SOSA)
    g.bind("xsd", XSD)
    g.bind("geo", GEO)
    g.bind("schema", SDO)

    for s, p, o in g.triples((None, GEO.asWKT, None)):
        if isinstance(o, Literal):
            wkt_text = str(o)
            try:
                coordinates = wkt_text.split('(')[-1].split(')')[0].split(' ')
                if len(coordinates) >= 2:
                    lat, long = coordinates[1], coordinates[0]
                    lat_decimal_length = len(lat.split('.')[-1]) if '.' in lat else 0
                    long_decimal_length = len(long.split('.')[-1]) if '.' in long else 0

                    lat_quality = assess_quality(lat_decimal_length)
                    long_quality = assess_quality(long_decimal_length)

                    result_bn_lat = BNode()
                    result_bn_long = BNode()

                    # Adding results for latitude
                    g.add((o, DQAF.hasDQAFResult, result_bn_lat))
                    g.add((result_bn_lat, DQAF.assessmentDate, Literal(assessment_date, datatype=XSD.date)))
                    g.add((result_bn_lat, SOSA.observedProperty, assessment_type))
                    g.add((result_bn_lat, SDO.value, Literal(f"Latitude: {lat_quality}")))

                    # Adding results for longitude
                    g.add((o, DQAF.hasDQAFResult, result_bn_long))
                    g.add((result_bn_long, DQAF.assessmentDate, Literal(assessment_date, datatype=XSD.date)))
                    g.add((result_bn_long, SOSA.observedProperty, assessment_type))
                    g.add((result_bn_long, SDO.value, Literal(f"Longitude: {long_quality}")))
            except IndexError:
                continue

    return g


from rdflib import Graph, URIRef, Literal, BNode, RDF
from rdflib.namespace import XSD
import re

# Assuming DQAF, GEO, SOSA, TIME, and SDO namespaces are already imported as before

def assess_coordinate_precision(g: Graph) -> Graph:
    assessment_type = URIRef("http://example.com/assessment/assess_coordinate_precision")
    assessment_date = datetime.now().date()

    g.bind("dqaf", DQAF)
    g.bind("sosa", SOSA)
    g.bind("xsd", XSD)
    g.bind("geo", GEO)
    g.bind("schema", SDO)

    for s, p, o in g.triples((None, GEO.hasGeometry, None)):
        geometry = None
        # Extracting the geometry as WKT Literal
        for s1, p1, o1 in g.triples((o, GEO.asWKT, None)):
            if p1 == GEO.asWKT:
                geometry = o1
                break

        if geometry:
            wkt_text = str(geometry)
            # Extracting coordinates from the WKT text
            try:
                # Assuming the WKT format is "POINT (lon lat)"
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", wkt_text)
                if match:
                    long, lat = match.groups()
                    lat_decimal_length = len(lat.split('.')[-1]) if '.' in lat else 0
                    long_decimal_length = len(long.split('.')[-1]) if '.' in long else 0

                    lat_quality = assess_quality(lat_decimal_length)
                    long_quality = assess_quality(long_decimal_length)

                    result_bn_lat = BNode()
                    result_bn_long = BNode()

                    # Adding results for latitude
                    g.add((s, DQAF.hasDQAFResult, result_bn_lat))
                    g.add((result_bn_lat, DQAF.assessmentDate, Literal(assessment_date, datatype=XSD.date)))
                    g.add((result_bn_lat, SOSA.observedProperty, assessment_type))
                    g.add((result_bn_lat, SDO.value, Literal(f"Latitude: {lat_quality}")))

                    # Adding results for longitude
                    g.add((s, DQAF.hasDQAFResult, result_bn_long))
                    g.add((result_bn_long, DQAF.assessmentDate, Literal(assessment_date, datatype=XSD.date)))
                    g.add((result_bn_long, SOSA.observedProperty, assessment_type))
                    g.add((result_bn_long, SDO.value, Literal(f"Longitude: {long_quality}")))
            except IndexError:
                continue

    return g


def assess_quality(decimal_length):
    if decimal_length > 4:
        return "HighQuality"
    elif 2 <= decimal_length <= 4:
        return "MediumQuality"
    else:
        return "LowQuality"
#####################################################