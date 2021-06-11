import concurrent.futures
import logging
import os
from abc import ABC, abstractmethod

from pyinsect.indexing.graph_index import GraphIndex
from pyinsect.structs.array_graph import ArrayGraph2D

logger = logging.getLogger(__name__)


class HPG(ABC):
    """An implementation of `Hierarchical Proximity Graph`"""

    def __init__(
        self,
        data,
        window_size,
        number_of_levels,
        similarity_metric,
        minimum_merging_margin=0.8,
        maximum_merging_margin=0.9,
        stride=1,
        deep_copy=False,
    ):
        self._window_size = window_size
        self._number_of_levels = number_of_levels
        self._stride = stride

        self._graph_indices = self._number_of_levels * [
            GraphIndex(
                similarity_metric,
                minimum_merging_margin=minimum_merging_margin,
                maximum_merging_margin=maximum_merging_margin,
                deep_copy=deep_copy,
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

    def __eq__(self, other):
        for (graph, other_graph) in zip(
            self._graphs_per_level, other._graphs_per_level
        ):
            if graph != other_graph:
                return False

        return True

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


class HPG2D(HPG):
    @classmethod
    def _clamp(cls, data, index):
        logger.debug("Clamping index %02d in the range [0, %02d]", index, len(data) - 1)

        return max(0, min(index, len(data) - 1))

    @classmethod
    def _get_window(cls, data, window_size, midpoint):
        logger.debug("Calculating the directional window of index %02d", midpoint)

        index_min = cls._clamp(data, midpoint - window_size // 2)
        index_max = cls._clamp(data, midpoint + window_size // 2)

        logger.debug(
            "The directional window of index %02d is [%02d, %02d]",
            midpoint,
            index_min,
            index_max,
        )

        return index_min, index_max

    @classmethod
    def _get_patch(cls, matrix, window_size, y, x):
        logger.debug("Processing patch (%02d, %02d)", y, x)

        y_min, y_max = cls._get_window(matrix, window_size, y)
        x_min, x_max = cls._get_window(matrix, window_size, x)

        return [
            [value for value in submatrix[x_min:x_max]]
            for submatrix in matrix[y_min:y_max]
        ]

    def _construct_neighborhood(
        self, x, y, data, window_size, graph_type, *args, **kwargs
    ):
        logger.debug(
            "Constructing the neighborhood of element %r at position (%02d, %02d)",
            data[y][x],
            y,
            x,
        )

        patch = self._get_patch(data, window_size, y, x)

        logger.debug(
            "Constructing an ArrayGraph2D<%r, %r, %r> with a window size of %02d from patch %r",
            graph_type,
            args,
            kwargs,
            window_size,
            patch,
        )

        return ArrayGraph2D(patch, window_size, self._stride).as_graph(
            graph_type, *args, **kwargs
        )

    def as_graph(self, graph_type, *args, **kwargs):
        logger.debug(
            "Constructing the initial ArrayGraph2D<%r, %r, %r> with a window size of %02d over data %r",
            graph_type,
            args,
            kwargs,
            self._window_size,
            self._data_per_lvl[0],
        )

        initial_graph = ArrayGraph2D(
            self._data_per_lvl[0], self._window_size, self._stride
        ).as_graph(graph_type, *args, **kwargs)

        self._graphs_per_level = [None] * (self._number_of_levels + 1)
        self._graphs_per_level[0] = initial_graph

        for lvl in range(1, self._number_of_levels + 1):
            # FIXME: Shouldn't lvl start from 2 due to
            # `initial_graph` being the 1st level
            # Check window_size as well as similarity calculation
            # implications of the above

            current_lvl_window_size = self._window_size * lvl

            previous_lvl_data = self._data_per_lvl[-1]

            number_of_neighborhoods = len(
                range(0, len(previous_lvl_data), self._stride)
            )

            logger.debug(
                "Level %02d consists of %02d number of neighborhoods over data %r",
                lvl,
                number_of_neighborhoods,
                previous_lvl_data,
            )

            # NOTE: Given a multi-level HPG and a `stride` > 1, `current_lvl_data` might end up
            # being a singleton 2D list (for example [[0]]). As a result, no edges are
            # going to be added to the current level graph.
            # See `ArrayGraph.as_graph`, for a better understanding of the situation.

            current_lvl_data = [[0] * number_of_neighborhoods] * number_of_neighborhoods

            for current_y, previous_y in enumerate(
                range(0, len(previous_lvl_data), self._stride)
            ):
                for current_x, previous_x in enumerate(
                    range(0, len(previous_lvl_data[previous_y]), self._stride)
                ):
                    neighborhood = self._construct_neighborhood(
                        previous_x,
                        previous_y,
                        previous_lvl_data,
                        current_lvl_window_size,
                        graph_type,
                        *args,
                        **kwargs
                    )

                    neighborhood_symbol = self._graph_indices[lvl - 1][neighborhood]

                    logger.debug(
                        "Assigning neighborhood (%02d, %02d) the symbol %r",
                        current_y,
                        current_x,
                        neighborhood_symbol,
                    )

                    current_lvl_data[current_y][current_x] = neighborhood_symbol

            self._data_per_lvl.append(current_lvl_data)

        for lvl in range(1, self._number_of_levels + 1):
            logger.debug(
                "Constructing an ArrayGraph2D<%r, %r, %r> with a window size of %02d from level %02d data %r",
                graph_type,
                args,
                kwargs,
                self._window_size * lvl,
                lvl,
                self._data_per_lvl[lvl],
            )

            current_lvl_graph = ArrayGraph2D(
                self._data_per_lvl[lvl], self._window_size * lvl, self._stride
            ).as_graph(graph_type, *args, **kwargs)

            self._graphs_per_level[lvl] = current_lvl_graph

        return self


class HPG2DParallel(HPG2D):
    def as_graph(self, graph_type, *args, pool=None, **kwargs):
        logger.debug(
            "Constructing the initial ArrayGraph2D<%r, %r, %r> with a window size of %02d over data %r",
            graph_type,
            args,
            kwargs,
            self._window_size,
            self._data_per_lvl[0],
        )

        initial_graph = ArrayGraph2D(
            self._data_per_lvl[0], self._window_size, self._stride
        ).as_graph(graph_type, *args, **kwargs)

        self._graphs_per_level = [None] * (self._number_of_levels + 1)
        self._graphs_per_level[0] = initial_graph

        for lvl in range(1, self._number_of_levels + 1):
            # FIXME: Shouldn't lvl start from 2 due to
            # `initial_graph` being the 1st level
            # Check window_size as well as similarity calculation
            # implications of the above

            current_lvl_window_size = self._window_size * lvl

            previous_lvl_data = self._data_per_lvl[-1]

            number_of_neighborhoods = len(
                range(0, len(previous_lvl_data), self._stride)
            )

            logger.debug(
                "Level %02d consists of %02d number of neighborhoods over data %r",
                lvl,
                number_of_neighborhoods,
                previous_lvl_data,
            )

            # NOTE: Given a multi-level HPG and a `stride` > 1, `current_lvl_data` might end up
            # being a singleton 2D list (for example [[0]]). As a result, no edges are
            # going to be added to the current level graph.
            # See `ArrayGraph.as_graph`, for a better understanding of the situation.

            current_lvl_data = [[0] * number_of_neighborhoods] * number_of_neighborhoods

            logger.debug(
                "Splitting neighborhood construction among %02d process", os.cpu_count()
            )

            futures = {}

            for current_y, previous_y in enumerate(
                range(0, len(previous_lvl_data), self._stride)
            ):
                for current_x, previous_x in enumerate(
                    range(0, len(previous_lvl_data[previous_y]), self._stride)
                ):
                    future = pool.submit(
                        self._construct_neighborhood,
                        previous_x,
                        previous_y,
                        previous_lvl_data,
                        current_lvl_window_size,
                        graph_type,
                        *args,
                        **kwargs
                    )

                    futures[future] = (current_y, current_x)

            # FIXME: we avoid utilizing `concurrent.futures.as_completed`
            # in this conctext, as the `GraphIndex` insertion order matters
            # for future in concurrent.futures.as_completed(futures):
            for future in futures:
                current_y, current_x = futures[future]

                logger.debug(
                    "The construction of neighborhood (%02d, %02d) has finished",
                    current_y,
                    current_x,
                )

                neighborhood = future.result()

                neighborhood_symbol = self._graph_indices[lvl - 1][neighborhood]

                logger.debug(
                    "Assigning neighborhood (%02d, %02d) the symbol %r",
                    current_y,
                    current_x,
                    neighborhood_symbol,
                )

                current_lvl_data[current_y][current_x] = neighborhood_symbol

            self._data_per_lvl.append(current_lvl_data)

        logger.debug(
            "Splitting per level graph construction among %02d process", os.cpu_count()
        )

        futures = {}

        for lvl in range(1, self._number_of_levels + 1):
            future = pool.submit(
                ArrayGraph2D(
                    self._data_per_lvl[lvl], self._window_size * lvl, self._stride
                ).as_graph,
                graph_type,
                *args,
                **kwargs
            )

            futures[future] = lvl

        for future in concurrent.futures.as_completed(futures):
            lvl = futures[future]

            graph_of_lvl = future.result()

            logger.debug(
                "The construction of the %02d level ArrayGraph2D<%r, %r, %r> with a window size of %02d over data %r has finished",
                lvl,
                graph_type,
                args,
                kwargs,
                self._window_size * lvl,
                self._data_per_lvl[lvl],
            )

            self._graphs_per_level[lvl] = graph_of_lvl

        return self
