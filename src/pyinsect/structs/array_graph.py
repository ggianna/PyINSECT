import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ArrayGraph(ABC):
    def __init__(self, data, window_size, stride=1) -> None:
        super().__init__()

        self._data = data
        self._window_size = window_size
        self._stride = stride

    def __len__(self):
        try:
            return len(self._graph)
        except AttributeError:
            return 0

    def __str__(self):
        return "length: {0}, window size: {1}, stride: {2}".format(
            len(self), self._window_size, self._stride
        )

    def __repr__(self) -> str:
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))

    @property
    def graph(self):
        return self._graph

    @property
    def window_size(self):
        return self._window_size

    @property
    def stride(self):
        return self._stride

    @abstractmethod
    def as_graph(self, graph_type, *args, **kwargs):
        raise NotImplementedError


class ArrayGraph2D(ArrayGraph):
    @classmethod
    def _clamp(cls, index, length):
        logger.debug("Clamping index %02d in the range [0, %02d]", index, length - 1)
        return max(0, min(index, length - 1))

    @classmethod
    def _get_window(cls, current_index, length, window_size):
        logger.debug("Calculating the directional window of index %02d", current_index)

        index_min = cls._clamp(current_index - window_size // 2, length)
        index_max = cls._clamp(current_index + window_size // 2, length)

        logger.debug(
            "The directional window of index %02d is [%02d, %02d]",
            current_index,
            index_min,
            index_max,
        )

        return index_min, index_max

    def _fetch_neighbors(self, current_y, current_x):
        logger.debug(
            "Fetching the neighbors of element (%02d, %02d)", current_y, current_x
        )

        neighbors = []

        y_min, y_max = self._get_window(current_y, len(self._data), self._window_size)

        for neighbor_y in range(y_min, y_max):
            x_min, x_max = self._get_window(
                current_x, len(self._data[neighbor_y]), self._window_size
            )
            for neighbor_x in range(x_min, x_max):
                if neighbor_x != current_x and neighbor_y != current_y:
                    logger.debug(
                        "Adding element %r at position (%02d, %02d) to the list of neighbors",
                        self._data[neighbor_y][neighbor_x],
                        neighbor_y,
                        neighbor_x,
                    )

                    neighbors.append(self._data[neighbor_y][neighbor_x])

        return neighbors

    def _process_patch(self, current_y, current_x):
        logger.debug("Processing patch (%02d, %02d)", current_y, current_x)

        current = self._data[current_y][current_x]

        edges = map(
            lambda neighbor: (current, neighbor),
            self._fetch_neighbors(current_y, current_x),
        )

        for vertex_a, vertex_b in edges:
            logger.debug("Creating an edge from %r to %r", vertex_a, vertex_b)
            self._graph.addEdgeInc((vertex_a,), (vertex_b,))

    def as_graph(self, graph_type, *args, **kwargs):
        logger.debug(
            "Instantiating an empty graph of type %r with args=%r and kwargs=%r",
            graph_type,
            args,
            kwargs,
        )

        self._graph = graph_type(*args, **kwargs)

        for current_y in range(0, len(self._data), self._stride):
            for current_x in range(0, len(self._data[current_y]), self._stride):
                self._process_patch(current_y, current_x)

        return self._graph
