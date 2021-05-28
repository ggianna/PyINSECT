from abc import ABC, abstractmethod

from pyinsect.documentModel.comparators.NGramGraphSimilarity import (
    SimilarityHPG,
    SimilarityNVS,
    SimilarityVS,
)
from pyinsect.documentModel.comparators.Operator import Union
from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph
from pyinsect.documentModel.representations.DocumentNGramHGraph import (
    DocumentNGramHGraph2D,
)


class GraphCollector(ABC):
    """
    An n-gram graph collector, which can create representative graphs of text/graph sets
    and can calculate appropriateness (essentially the similarity) of a text, with respect
    to the representative graph.
    """

    def __init__(self, similarity_metric):
        self._number_of_docs = 0
        self._representative_graph = None

        self._similarity_metric = similarity_metric

    def __len__(self):
        return self._number_of_docs

    def __str__(self):
        return "number of documents: {0}, similarity metric: {1}".format(
            self._number_of_docs, self._similarity_metric.__class__.__name__
        )

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))

    @property
    def representative_graph(self):
        return self._representative_graph

    def _add_graph(self, graph, deep_copy=False):
        """Adds the graph input to the representative graph."""

        if self._number_of_docs == 0:
            self._representative_graph = graph
        else:
            bop = Union(
                lf=1 / (self._number_of_docs + 1), commutative=True, distributional=True
            )

            self._representative_graph = bop.apply(
                self._representative_graph, graph, dc=deep_copy
            )

        self._number_of_docs += 1

    def _appropriateness_of_graph(self, graph):
        """
        Returns a degree of `appropriateness` of a graph, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the graph to the representative graph.
        """

        # FIXME: In my humble opinion the logic of appropriateness calculation
        # should be moved outside of the data collection module

        return self._similarity_metric(graph, self._representative_graph)

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def appropriateness_of(self, *args, **kwargs):
        raise NotImplementedError


class NGramGraphCollector(GraphCollector):
    def __init__(self):
        super().__init__(SimilarityNVS())

    def add(self, text, deep_copy=False, n=3, window_size=3):
        """Adds the graph of the input text to the representative graph."""

        graph = DocumentNGramGraph(n, window_size, text)

        self._add_graph(graph, deep_copy=deep_copy)

    def appropriateness_of(self, text, n=3, window_size=3):
        """
        Returns a degree of `appropriateness` of a text, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the text to the representative graph.
        """

        # FIXME: In my humble opinion the logic of appropriateness calculation
        # should be moved outside of the data collection module

        graph = DocumentNGramGraph(n, window_size, text)

        return self._appropriateness_of_graph(graph)
