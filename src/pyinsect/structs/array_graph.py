from abc import ABC, abstractmethod

import networkx


class ArrayGraph(ABC):
    def __init__(self, data, window_size) -> None:
        super().__init__()

        self._data = data
        self._window_size = window_size

    def __len__(self):
        try:
            return self._graph.size()
        except AttributeError:
            return 0

    def __str__(self):
        return "length: {0}, window: {1}".format(len(self), self._window_size)

    def __repr__(self) -> str:
        return '<{0} "{1}">'.format(self.__class__.__name__, str(self))

    @property
    def graph(self):
        return self._graph

    @property
    def window_size(self):
        return self._window_size

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

    def _process_patch(self, x, y):
        neighbors = []

        for neighbor_y in range(*self._get_window(y)):
            for neighbor_x in range(*self._get_window(x)):
                if neighbor_x != x and neighbor_y != y:
                    neighbors.append((neighbor_y, neighbor_x))

        return neighbors

    def as_graph(self, graph_type, *args, **kwargs):
        self._graph = graph_type(*args, **kwargs)
        self._graph._Graph = networkx.DiGraph()

        for y in range(len(self._data)):
            for x in range(len(self._data)):
                current = self._data[y][x]
                for neighbor_y, neighbor_x in self._process_patch(x, y):
                    neighbor = self._data[neighbor_y][neighbor_x]
                    self._graph.addEdgeInc((str(current),), (str(neighbor),))

        return self._graph
