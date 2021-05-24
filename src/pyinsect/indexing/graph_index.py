from pyinsect.documentModel.comparators.Operator import Union
from pyinsect.documentModel.comparators.Operator import (
    inverse_intersection as AllNotIn,
)


class GraphIndex(object):
    def __init__(
        self, similarity_metric, minimum_merging_margin=0.8, maximum_merging_margin=0.9
    ):
        super().__init__()

        self.minimum_merging_margin = minimum_merging_margin
        self.maximum_merging_margin = maximum_merging_margin
        self.similarity_metric = similarity_metric

        self._graph_index = []

        self.all_not_in = AllNotIn()

    def __getitem__(self, graph):
        matching_index = -1

        for index, (other_graph, count) in enumerate(self._graph_index):
            similarity = self.similarity_metric.apply(graph, other_graph)

            if similarity >= self.maximum_merging_margin:
                matching_index = index
                break

            if similarity >= self.minimum_merging_margin:
                union = Union(lf=1 - (count / (count + 1)))

                other_graph = union.apply(graph, other_graph)
                count = count + 1

                self._graph_index[index] = (other_graph, count)

                matching_index = index
                break

            if 1.0 - similarity > 10e-5:
                graph = self.all_not_in.apply(other_graph, graph)

        if matching_index < 0:
            matching_index = len(self._graph_index)

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
