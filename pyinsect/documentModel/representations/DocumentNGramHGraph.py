import networkx as nx
from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph


class DocumentNGramHSubGraph(DocumentNGramGraph):
    def __init__(self, n=3, Dwin=2, Data=[], GPrintVerbose=True, child=None):
        self.symbols = []
        self.child = child

        super().__init__(n=n, Dwin=Dwin, Data=Data, GPrintVerbose=GPrintVerbose)

        if self._Graph is None:
            self._Graph = nx.DiGraph()

    def buildGraph(self, verbose=False, d=[]):
        super().buildGraph(verbose=verbose, d=d)

        for node in self._Graph.nodes:
            subset = [node] + list(self._Graph.neighbors(node))
            subgraph = self._Graph.subgraph(subset)
            self.symbols.append(subgraph)

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

        super().__init__(n=n, Dwin=Dwin, Data=Data, GPrintVerbose=GPrintVerbose)

        if self._Graph is None:
            self._Graph = nx.DiGraph()

    def buildGraph(self, verbose=False, d=[]):
        child, sequence = None, self._Data
        if self.levels > 1:
            for level in range(1, self.levels):
                window_size = int(self._Dwin * level)

                child = DocumentNGramHSubGraph(
                    n=self._n,
                    Dwin=window_size,
                    Data=sequence,
                    GPrintVerbose=True,
                    child=child,
                )

                sequence = list(range(len(child.symbols)))

            self._Dwin = int(self._Dwin * (level + 1))

        self.child = child

        return super().buildGraph(verbose=verbose, d=sequence)
