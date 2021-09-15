import concurrent
import unittest

from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph
from pyinsect.documentModel.representations.hpg import HPG2D, HPG2DParallel
from tests.base import BaseParallelTestCase, BaseTestCase
from tests.hpg.base import HPGTestCaseMixin


class HPG2DTestCase(HPGTestCaseMixin, BaseTestCase):
    graph_type = HPG2D


class HPG2DParallelTestCase(HPGTestCaseMixin, BaseParallelTestCase):
    graph_type = HPG2DParallel

    def _construct_graph(
        self, data, window_size, number_of_levels, similarity_metric, *args, **kwargs
    ):
        return super()._construct_graph(
            data,
            window_size,
            number_of_levels,
            similarity_metric,
            *args,
            pool=self.pool,
            **kwargs
        )

    def test_equality_non_parallel(self):
        graph1 = HPG2D(self.data, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        graph2 = self._construct_graph(self.data, 3, 3, self.array_graph_metric)

        self.assertEqual(graph1, graph2)

    def test_concurrency_on_graph_construction(self):
        self._construct_graph(self.data, 3, 3, self.array_graph_metric)

    @unittest.skip("due to `TypeError: cannot pickle '_io.TextIOWrapper' object`")
    def test_concurrency_on_all_levels(self):
        futures = []

        for _ in range(2):
            future = self.pool.submit(
                self._construct_graph,
                self.data,
                3,
                3,
                self.array_graph_metric,
            )

            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            future.result()
