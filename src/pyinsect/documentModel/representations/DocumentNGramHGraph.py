import logging
from abc import ABC, abstractmethod

from pyinsect.indexing.graph_index import GraphIndex
from pyinsect.structs.array_graph import ArrayGraph2D

logger = logging.getLogger(__name__)


class DocumentNGramHGraph(ABC):
    def __init__(
        self,
        data,
        window_size,
        number_of_levels,
        similarity_metric,
        minimum_merging_margin=0.8,
        maximum_merging_margin=0.9,
        stride=1,
    ):
        self._window_size = window_size
        self._number_of_levels = number_of_levels
        self._stride = stride

        self._graph_indices = self._number_of_levels * [
            GraphIndex(
                similarity_metric,
                minimum_merging_margin=minimum_merging_margin,
                maximum_merging_margin=maximum_merging_margin,
            )
        ]

        self._data_per_lvl = [
            data,
        ]

        self._graphs_per_level = []

    def __len__(self):
        size = 0
        for graph in self._graphs_per_level:
            size += len(graph)

        return size

    def __getitem__(self, index):
        return self._graphs_per_level[index]

    def __iter__(self):
        yield from self._graphs_per_level

    def __str__(self):
        return (
            "length: {0}, window size: {1}, stride: {2}, number of levels: {3}".format(
                len(self), self._window_size, self._stride, self._number_of_levels
            )
        )

    def __repr__(self) -> str:
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))

    @property
    def window_size(self):
        return self._window_size

    @property
    def stride(self):
        return self._stride

    @property
    def number_of_levels(self):
        return self._number_of_levels

    @abstractmethod
    def as_graph(self, graph_type, *args, **kwargs):
        raise NotImplementedError


class DocumentNGramHGraph2D(DocumentNGramHGraph):
    @classmethod
    def _clamp(cls, data, index):
        return max(0, min(index, len(data) - 1))

    @classmethod
    def _get_window(cls, data, window_size, midpoint):
        index_min = cls._clamp(data, midpoint - window_size // 2)
        index_max = cls._clamp(data, midpoint + window_size // 2)

        return index_min, index_max

    @classmethod
    def _get_patch(cls, matrix, window_size, y, x):
        y_min, y_max = cls._get_window(matrix, window_size, y)
        x_min, x_max = cls._get_window(matrix, window_size, x)

        return [
            [value for value in submatrix[x_min:x_max]]
            for submatrix in matrix[y_min:y_max]
        ]

    def as_graph(self, graph_type, *args, **kwargs):
        initial_graph = ArrayGraph2D(
            self._data_per_lvl[0], self._window_size, self._stride
        ).as_graph(graph_type, *args, **kwargs)

        self._graphs_per_level.append(initial_graph)

        for lvl in range(1, self._number_of_levels + 1):
            # FIXME: Shouldn't lvl start from 2 due to
            # `initial_graph` being the 1st level
            # Check window_size as well as similarity calculation
            # implications of the above

            logger.debug("Level: %02d", lvl)

            current_lvl_window_size = self._window_size * lvl

            previous_lvl_data = self._data_per_lvl[-1]

            number_of_neighborhoods = len(
                range(0, len(previous_lvl_data), self._stride)
            )

            # NOTE: Given a multi-level HPG and a `stride` > 1, `current_lvl_data` might end up
            # being a singleton 2D list (for example [[0]]). As a result, no edges are
            # going to be added to the current level graph.
            # See `ArrayGraph.as_graph`, for a better understanding of the situation.

            current_lvl_data = [[0] * number_of_neighborhoods] * number_of_neighborhoods

            for current_y, previous_y in enumerate(
                range(0, len(previous_lvl_data), self._stride)
            ):
                logger.debug("Current row: %02d", previous_y)

                for current_x, previous_x in enumerate(
                    range(0, len(previous_lvl_data[previous_y]), self._stride)
                ):
                    logger.debug("Current column: %02d", previous_x)

                    patch = self._get_patch(
                        previous_lvl_data,
                        current_lvl_window_size,
                        previous_y,
                        previous_x,
                    )

                    neighborhood = ArrayGraph2D(
                        patch, current_lvl_window_size, self._stride
                    ).as_graph(graph_type, *args, **kwargs)

                    neighborhood_symbol = self._graph_indices[lvl - 1][neighborhood]

                    current_lvl_data[current_y][current_x] = neighborhood_symbol

            self._data_per_lvl.append(current_lvl_data)

            current_lvl_graph = ArrayGraph2D(
                current_lvl_data, current_lvl_window_size, self._stride
            ).as_graph(graph_type, *args, **kwargs)

            self._graphs_per_level.append(current_lvl_graph)

        return self
