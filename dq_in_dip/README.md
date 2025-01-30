This directory gives a minimal example of:
1. converting individual assessments to SPARQL, and
2. converting the inputs to an assessment to SPARQL

The assessments are implemented as pytest tests, and a fixture is used to serialise the results.

The tests can be run with, from the repo root:

`pytest dq_in_dip/ -o pythonpath=.`
`poetry run pytest dq_in_dip/ -o pythonpath=.`

etc.