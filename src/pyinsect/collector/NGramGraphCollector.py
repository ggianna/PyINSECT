from abc import ABC, abstractmethod

from pyinsect.documentModel.comparators.NGramGraphSimilarity import (
    SimilarityHPG,
    SimilarityNVS,
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

        self._similarity_metric = similarity_metric

    def __len__(self):
        return self._number_of_docs

    def __str__(self):
        return "number of documents: {0}, similarity metric: {1}".format(
            self._number_of_docs, self._similarity_metric.__class__.__name__
        )

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))

    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def appropriateness_of(self, *args, **kwargs):
        raise NotImplementedError


class NGramGraphCollectorBase(GraphCollector):
    def __init__(
        self,
        similarity_metric,
        n=3,
        window_size=3,
        deep_copy=False,
        commutative=True,
        distributional=True,
    ):
        super().__init__(similarity_metric)

        self._deep_copy = deep_copy
        self._n = n
        self._window_size = window_size

        self._commutative = commutative
        self._distributional = distributional

        self._representative_graph = None

    def __str__(self):
        return "{0}, n-gram rank: {1}, window size: {2}".format(
            super().__str__(), self._n, self._window_size
        )

    def add(self, text):
        """Adds the graph of the input text to the representative graph."""

        graph = DocumentNGramGraph(self._n, self._window_size, text)

        self._add_graph(graph)

    def appropriateness_of(self, text):
        """
        Returns a degree of `appropriateness` of a text, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the text to the representative graph.
        """

        # FIXME: In my humble opinion the logic of appropriateness calculation
        # should be moved outside of the data collection module

        graph = DocumentNGramGraph(self._n, self._window_size, text)

        return self._appropriateness_of_graph(graph)

    def _add_graph(self, graph):
        """Adds the graph input to the representative graph."""

        if self._number_of_docs == 0:
            self._representative_graph = graph
        else:
            union = Union(
                lf=1 / (self._number_of_docs + 1),
                commutative=self._commutative,
                distributional=self._distributional,
            )

            self._representative_graph = union.apply(
                self._representative_graph, graph, dc=self._deep_copy
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


class NGramGraphCollector(NGramGraphCollectorBase):
    def __init__(
        self, n=3, window_size=3, deep_copy=False, commutative=True, distributional=True
    ):
        super().__init__(
            SimilarityNVS(),
            n=n,
            window_size=window_size,
            deep_copy=deep_copy,
            commutative=commutative,
            distributional=distributional,
        )


class HPG2DCollectorBase(GraphCollector):
    def __init__(
        self,
        similarity_metric,
        graph_type,
        *args,
        window_size=3,
        number_of_levels=3,
        minimum_merging_margin=0.8,
        maximum_merging_margin=0.9,
        stride=1,
        **kwargs
    ):
        super().__init__(SimilarityHPG(similarity_metric))

        self._window_size = window_size
        self._number_of_levels = number_of_levels
        self._per_graph_similarity_metric = similarity_metric
        self._minimum_merging_margin = minimum_merging_margin
        self._maximum_merging_margin = maximum_merging_margin
        self._stride = stride

        self._graph_type = graph_type
        self._per_graph_args = args
        self._per_graph_kwargs = kwargs

        self._graphs = []

    def __str__(self):
        return "{0}, window size: {1}, stride: {2}, number of levels: {3}, graph type: {4}".format(
            super().__str__(),
            self._window_size,
            self._stride,
            self._number_of_levels,
            self._graph_type,
        )

    def add(self, matrix_2d):
        graph = DocumentNGramHGraph2D(
            matrix_2d,
            self._window_size,
            self._number_of_levels,
            self._similarity_metric,
            minimum_merging_margin=self._minimum_merging_margin,
            maximum_merging_margin=self._maximum_merging_margin,
            stride=self._stride,
        ).as_graph(self._graph_type, *self._per_graph_args, **self._per_graph_kwargs)

        self._add_graph(graph)

    def appropriateness_of(self, matrix_2d):
        graph = DocumentNGramHGraph2D(
            matrix_2d,
            self._window_size,
            self._number_of_levels,
            self._similarity_metric,
            minimum_merging_margin=self._minimum_merging_margin,
            maximum_merging_margin=self._maximum_merging_margin,
            stride=self._stride,
        ).as_graph(self._graph_type, *self._per_graph_args, **self._per_graph_kwargs)

        return self._appropriateness_of_graph(graph)

    def _add_graph(self, graph):
        self._graphs.append(graph)

    def _appropriateness_of_graph(self, graph):
        similarity = 0

        for other_graph in self._graphs:
            similarity += self._similarity_metric(other_graph, graph) / len(
                self._graphs
            )

        return similarity


class HPG2DCollector(HPG2DCollectorBase):
    def __init__(self, window_size=2, number_of_levels=5, stride=4):
        super().__init__(
            SimilarityNVS(),
            DocumentNGramGraph,
            window_size=window_size,
            number_of_levels=number_of_levels,
            stride=stride,
        )
