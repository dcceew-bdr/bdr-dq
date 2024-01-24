import pytest
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import SDO
from rdflib.plugins.parsers.notation3 import BadSyntax
from dq.__main__ import load_data, assessment_01
from pathlib import Path


def test_load_data_01():
    g = load_data(Path(__file__).parent / "data" / "eg_01.ttl")

    assert isinstance(g, Graph)


def test_load_data_02():
    with pytest.raises(BadSyntax):
        g = load_data(Path(__file__).parent / "data" / "eg_02.ttl")

        assert isinstance(g, Graph)


def test_load_data_03():
    g = Graph().parse(str(Path(__file__).parent / "data" / "eg_01.ttl"))
    g2 = load_data(g)

    assert isinstance(g2, Graph)


def test_load_data_04():
    with pytest.raises(FileNotFoundError):
        g = load_data(Path("fake path"))

        assert isinstance(g, Graph)


def test_load_data_05():
    with pytest.raises(TypeError):
        g = load_data()

        assert isinstance(g, Graph)


def test_assessment_01_01():
    g = Graph().parse(str(Path(__file__).parent / "data" / "eg_01.ttl"))
    result = assessment_01(g)

    assert (
        URIRef("http://example.com/thingWithResult"),
        URIRef("https://linked.data.gov.au/def/bdr/dqaf/hasDQAFResult"),
        None
    ) in result


def test_assessment_01_02():
    g = Graph().parse(str(Path(__file__).parent / "data" / "eg_03.ttl"))
    result = assessment_01(g)
    actual_count = None

    for o in result.objects(URIRef("http://example.com/thingWithResult"), URIRef("https://linked.data.gov.au/def/bdr/dqaf/hasDQAFResult")):
        for o2 in result.objects(o, SDO.value):
            actual_count = int(o2)

    assert actual_count == 5
