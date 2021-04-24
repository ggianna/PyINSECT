from functools import reduce

from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph


class DocumentNGramHSubGraph(DocumentNGramGraph):
    def __init__(self, n=3, Dwin=2, Data=[], GPrintVerbose=True):
        self.lookup_table = []

        super().__init__(n=n, Dwin=Dwin, Data=Data, GPrintVerbose=GPrintVerbose)

    def buildGraph(self, verbose=False, d=[]):
        super().buildGraph(verbose=verbose, d=d)

        for node in self._Graph.nodes:
            subset = [node] + list(self._Graph.neighbors(node))
            subgraph = self._Graph.subgraph(subset)
            self.lookup_table.append(subgraph)

        return self._Graph

    def addEdgeInc(self, a, b, w=1):
        # A = repr(a)#str(a)
        # B = repr(b)#str(b)
        # merging can also be done in other ways
        # add an extra class variable
        A, B = tuple(a), tuple(b)
        if (A, B) in self._edges:
            edata = self._Graph.get_edge_data(A, B)
            # DEBUG LINES
            # print "updating edge between (",A,B,")"
            # print "to weight",(edata['weight']+1)

            r = edata["weight"] + w
        else:
            # DEBUG LINES
            # print "adding edge between (",A,B,")"

            r = w
        # update/add edge weight
        self.setEdge(A, B, r)


class DocumentNGramHGraph(DocumentNGramHSubGraph):
    def __init__(self, levels, n=3, Dwin=2, Data=[], GPrintVerbose=True):
        self.levels = levels
        self.original_data = Data
        self.subgraphs = []

        super().__init__(n=n, Dwin=Dwin, Data=Data, GPrintVerbose=GPrintVerbose)

    def buildGraph(self, verbose=False, d=[]):
        sequence = self._Data
        for level in range(1, self.levels):
            window_size = int(self._Dwin * level)

            document_n_gram_graph = DocumentNGramHSubGraph(
                n=self._n, Dwin=window_size, Data=sequence, GPrintVerbose=True
            )

            self.subgraphs.append(document_n_gram_graph)
            sequence = document_n_gram_graph.lookup_table

        if self.levels > 1:
            self._Dwin = int(self._Dwin * (level + 1))

        self.subgraphs = self.subgraphs[::-1]

        return super().buildGraph(verbose=verbose, d=sequence)
