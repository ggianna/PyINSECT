import logging

from pyinsect.documentModel.comparators.Operator import Union
from pyinsect.documentModel.comparators.Operator import inverse_intersection as AllNotIn

logger = logging.getLogger(__name__)


class GraphIndex(object):
    def __init__(
        self,
        similarity_metric,
        minimum_merging_margin=0.8,
        maximum_merging_margin=0.9,
        deep_copy=False,
    ):
        super().__init__()

        self.similarity_metric = similarity_metric

        self.minimum_merging_margin = minimum_merging_margin
        self.maximum_merging_margin = maximum_merging_margin

        self._deep_copy = deep_copy

        self._graph_index = []

        self.all_not_in = AllNotIn()

    def __getitem__(self, graph):
        logger.debug("Inserting graph %s", graph)

        matching_index = -1

        for index, (other_graph, count) in enumerate(self._graph_index):
            logger.debug(
                "Comparing graph %s with graph %s on index %02d",
                graph,
                other_graph,
                index,
            )

            similarity = self.similarity_metric(graph, other_graph)

            logger.debug(
                "The similarity between graph %s and %s is %05.3f",
                graph,
                other_graph,
                similarity,
            )

            if similarity >= self.maximum_merging_margin:
                logger.debug("Found matching index %02d for graph %s", index, graph)
                matching_index = index
                break

            if similarity >= self.minimum_merging_margin:
                logger.debug(
                    "Found near perfect matching index %02d for graph %s", index, graph
                )
                union = Union(lf=1 - (count / (count + 1)))

                logger.debug(
                    "Merging graph %s into existing graph %s", graph, other_graph
                )
                other_graph = union(other_graph, graph, dc=self._deep_copy)
                count = count + 1

                self._graph_index[index] = (other_graph, count)

                matching_index = index
                break

            if 1.0 - similarity > 10e-5:
                logger.debug(
                    "No match yet. Perform inversely intersect graph %s with existing graph %s",
                    graph,
                    other_graph,
                )
                graph = self.all_not_in(graph, other_graph, dc=self._deep_copy)

        if matching_index < 0:
            matching_index = len(self._graph_index)

            logger.debug(
                "No match for graph %s. Creating a new entry at index %02d",
                graph,
                matching_index,
            )

            self._graph_index.append((graph, 1))

        return matching_index

    def __iter__(self):
        yield from self._graph_index

    def __len__(self):
        return len(self._graph_index)

    def __str__(self):
        return "length: {0}".format(
            len(self),
        )

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))
