import logging
from abc import ABC, abstractmethod

from pyinsect.documentModel.comparators.NGramGraphSimilarity import (
    SimilarityHPG,
    SimilarityNVS,
)
from pyinsect.documentModel.comparators.Operator import Union
from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph
from pyinsect.documentModel.representations.DocumentNGramSymWinGraph import (
    DocumentNGramSymWinGraph,
)
from pyinsect.documentModel.representations.hpg import HPG2D, HPG2DParallel
from pyinsect.structs.array_graph import ArrayGraph2D

logger = logging.getLogger(__name__)


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

        logger.debug("Constructing graph from %s", text)
        graph = self._construct_graph(text)

        logger.debug("Adding graph %s", graph)
        self._add_graph(graph)

    def appropriateness_of(self, text):
        """
        Returns a degree of `appropriateness` of a text, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the text to the representative graph.
        """

        logger.debug("Constructing graph from %s", text)
        graph = self._construct_graph(text)

        logger.debug("Calculating the appropriateness of graph %s", graph)
        return self._appropriateness_of_graph(graph)

    def _construct_graph(self, data, *args, **kwargs):
        return DocumentNGramGraph(self._n, self._window_size, data)

    def _add_graph(self, graph):
        """Adds the graph input to the representative graph."""

        if self._number_of_docs == 0:
            logger.debug(
                "No documents parsed yet. Assigning %s as the representative graph",
                graph,
            )
            self._representative_graph = graph
        else:
            union = Union(
                lf=1 / (self._number_of_docs + 1),
                commutative=self._commutative,
                distributional=self._distributional,
            )

            logger.debug(
                "Merging graph %s into representative graph %s (deep_copy=%r)",
                graph,
                self._representative_graph,
                self._deep_copy,
            )
            self._representative_graph = union.apply(
                self._representative_graph, graph, dc=self._deep_copy
            )

        logging.debug(
            "Incrementing the number of documents to %02d", self._number_of_docs
        )
        self._number_of_docs += 1

    def _appropriateness_of_graph(self, graph):
        """
        Returns a degree of `appropriateness` of a graph, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the graph to the representative graph.
        """

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


class ArrayGraph2DCollector(NGramGraphCollector):
    def __init__(
        self,
        n=3,
        window_size=3,
        deep_copy=False,
        commutative=True,
        distributional=True,
        stride=1,
    ):
        super().__init__(
            n=n,
            window_size=window_size,
            deep_copy=deep_copy,
            commutative=commutative,
            distributional=distributional,
        )

        self._stride = stride

    def __str__(self):
        return "{0}, stride: {1}".format(super().__str__(), self._stride)

    def _construct_graph(self, data, *args, **kwargs):
        return ArrayGraph2D(data, self._window_size, stride=self._stride).as_graph(
            DocumentNGramGraph, self._n, self._window_size
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
        logger.debug("Constructing graph from %s", matrix_2d)

        graph = self._construct_graph(matrix_2d)

        logger.debug("Adding graph %s", graph)
        self._add_graph(graph)

    def appropriateness_of(self, matrix_2d):
        logger.debug("Constructing graph from %s", matrix_2d)

        graph = self._construct_graph(matrix_2d)

        logger.debug("Calculating the appropriateness of graph %s", graph)
        return self._appropriateness_of_graph(graph)

    def _construct_graph(self, data, *args, **kwargs):
        return HPG2D(
            data,
            self._window_size,
            self._number_of_levels,
            self._per_graph_similarity_metric,
            minimum_merging_margin=self._minimum_merging_margin,
            maximum_merging_margin=self._maximum_merging_margin,
            stride=self._stride,
        ).as_graph(self._graph_type, *self._per_graph_args, **self._per_graph_kwargs)

    def _add_graph(self, graph):
        logger.debug("Appending graph %s to the list of graphs", graph)
        self._graphs.append(graph)

    def _appropriateness_of_graph(self, graph):
        similarity = 0

        for index, other_graph in enumerate(self._graphs):
            logger.debug(
                "Calculating the '%r' similarity on level %02d between graph %s and graph %s",
                self._similarity_metric,
                index,
                graph,
                other_graph,
            )

            current_similarity = self._similarity_metric(other_graph, graph) / len(
                self._graphs
            )

            logger.debug(
                "The '%r' similarity on level %02d between graph %s and graph %s is %05.3f",
                self._similarity_metric,
                index,
                graph,
                other_graph,
                current_similarity,
            )

            similarity += current_similarity

            logger.debug(
                "The overall similarity of graph %s and graph %s is %05.3f",
                graph,
                other_graph,
                similarity,
            )

        return similarity


class HPG2DCollector(HPG2DCollectorBase):
    def __init__(self, window_size=2, number_of_levels=5, stride=1, **kwargs):
        super().__init__(
            SimilarityNVS(),
            DocumentNGramSymWinGraph,
            window_size=window_size,
            number_of_levels=number_of_levels,
            stride=stride,
            **kwargs
        )


class HPG2DCollectorParallel(HPG2DCollector):
    def _construct_graph(self, data, *args, **kwargs):
        return HPG2DParallel(
            data,
            self._window_size,
            self._number_of_levels,
            self._per_graph_similarity_metric,
            minimum_merging_margin=self._minimum_merging_margin,
            maximum_merging_margin=self._maximum_merging_margin,
            stride=self._stride,
        ).as_graph(self._graph_type, *self._per_graph_args, **self._per_graph_kwargs)
