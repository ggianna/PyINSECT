import unittest

from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph
from pyinsect.documentModel.representations.hpg import HPG2D, HPG2DParallel
from tests.hpg.base import HPGTestCaseMixin


class HPG2DTestCase(HPGTestCaseMixin, unittest.TestCase):
    graph_type = HPG2D


class HPG2DParallelTestCase(HPGTestCaseMixin, unittest.TestCase):
    graph_type = HPG2DParallel

    def test_equality_non_parallel(self):
        graph1 = HPG2D(self.data, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        graph2 = self.graph_type(self.data, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        self.assertEqual(graph1, graph2)
