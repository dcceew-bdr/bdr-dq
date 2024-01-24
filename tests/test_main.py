import pytest
from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax
from dq.__main__ import one


def test_one_01():
    g = Graph().parse(
        data="""
            PREFIX ex: <http://example.com/>
            PREFIX schema: <https://schema.org/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            
            ex:eg001
                a schema:Person ;
                schema:name "Nicholas Car" ;
                schema:email "nicholas.car@dccees.gov.au"^^xsd:anyURI ;
            .
            """,
        format="turtle"
    )

    assert one(g) == 3


def test_one_02():
    with pytest.raises(BadSyntax):
        g = Graph().parse(
            data="""
                PREFIX ex: <http://example.com/>
                PREFIX schema: <https://schema.org/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
                ex:eg001
                    a schema:Person ;
                    schema:name "Nicholas Car" ;
                    schema:email "nicholas.car@dccees.gov.au"^^xsd:anyURI ;
                
                """,
            format="turtle"
        )

        assert one(g) == 3
