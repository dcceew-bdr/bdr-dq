The data quality assessment can be run as a python script with:

`uv run python Convert/main.py "Old Implementation/SPARQL Codes and Tests/chunk_1 samplae input data for test.ttl" --scope BDR`

The scope must be one of:
1. Chunk
2. Dataset
3. BDR

This will:
- log which assessments are run to STDOUT
- produce two output files in Convert/output:
    1. The DQAF results with a compressed literal
    2. Metadata describing