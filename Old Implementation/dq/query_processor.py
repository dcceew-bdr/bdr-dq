import rdflib


class RDFQueryProcessor:
    def __init__(self, filepath, format="turtle"):
        self.graph = rdflib.Graph()
        self.graph.parse(filepath, format=format)

    def execute_query(self, out_p_uri, aus_st_uri, out_p_value="normal", aus_st_value="Western_Australia"):
        query = f"""
        PREFIX out_p: <{out_p_uri}>
        

        SELECT ?subject
        WHERE {{
          ?subject out_p:property "{out_p_value}"
                   .
        }}
        """
        return self.graph.query(query)

    def print_results(self, results):
        for row in results:
            print(row.subject)