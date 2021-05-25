from abc import ABC, abstractmethod

import networkx


class ArrayGraph(ABC):
    def __init__(self, data, window_size, stride=1) -> None:
        super().__init__()

        self._data = data
        self._window_size = window_size
        self._stride = stride

    def __len__(self):
        try:
            return self._graph.size()
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
    def _clamp(self, index):
        return max(0, min(index, len(self._data) - 1))

    def _get_window(self, center):
        index_min = self._clamp(center - self._window_size // 2)
        index_max = self._clamp(center + self._window_size // 2)

        return index_min, index_max

    def _fetch_neighbors(self, current_y, current_x):
        neighbors = []

        for neighbor_y in range(*self._get_window(current_y), self._stride):
            for neighbor_x in range(*self._get_window(current_x), self._stride):
                if neighbor_x != current_x and neighbor_y != current_y:
                    neighbors.append(self._data[neighbor_y][neighbor_x])

        return neighbors

    def _process_patch(self, current_y, current_x):
        return map(
            lambda neighbor: (self._data[current_y][current_x], neighbor),
            self._fetch_neighbors(current_y, current_x),
        )

    def as_graph(self, graph_type, *args, **kwargs):
        self._graph = graph_type(*args, **kwargs)

        for y in range(len(self._data)):
            for x in range(len(self._data)):
                for vertex_a, vertex_b in self._process_patch(y, x):
                    self._graph.addEdgeInc((vertex_a,), (vertex_b,))

        return self._graph
