import itertools
import logging
import random
import string
import unittest

from pyinsect.documentModel.comparators import SimilarityHPG, SimilarityVS
from pyinsect.documentModel.representations import (
    DocumentNGramGraph,
    DocumentNGramHGraph2D,
)


def generate_random_2d_int_array(size):
    return [
        [
            ord(random.choice(string.ascii_letters)) for y in range(size)
        ] for x in range(size)
    ]

class DocumentNGramHGraphTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=logging.DEBUG,
    )

    def setUp(self):
        random.seed(1234)

        self.data = generate_random_2d_int_array(5)

        self.array_graph_metric = SimilarityVS()
        self.hpg_metric = SimilarityHPG(SimilarityVS)

    def test_same_similarity(self):
        graph1 = DocumentNGramHGraph2D(self.data, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        graph2 = DocumentNGramHGraph2D(self.data, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        value = self.hpg_metric.apply(graph1, graph2)

        self.assertEqual(value, 1.0)

    def test_diff_similarity(self):
        for permutation in itertools.permutations(self.data):
            if permutation == tuple(self.data):
                continue

            with self.subTest(permutation=permutation):
                graph1 = DocumentNGramHGraph2D(
                    permutation, 3, 3, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                graph2 = DocumentNGramHGraph2D(
                    self.data, 3, 3, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                value = self.hpg_metric.apply(graph1, graph2)

                self.logger.debug("%s %s %4.3f", self.data, permutation, value)

                self.assertNotEqual(value, 1.0)

    def test_commutativity(self):
        length1 = random.randint(1, len(string.ascii_letters))
        length2 = random.randint(1, len(string.ascii_letters))

        data1 = generate_random_2d_int_array(length1)
        data2 = generate_random_2d_int_array(length2)

        graph1 = DocumentNGramHGraph2D(data1, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        graph2 = DocumentNGramHGraph2D(data2, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        value1 = self.hpg_metric.apply(graph1, graph2)
        value2 = self.hpg_metric.apply(graph2, graph1)

        self.assertEqual(value1, value2)

    def test_combinations(self):
        for _ in range(10):
            length1 = random.randint(1, len(string.ascii_letters))
            length2 = random.randint(1, len(string.ascii_letters))

            data1 = generate_random_2d_int_array(length1)
            data2 = generate_random_2d_int_array(length2)

            levels1, Dwin1 = (
                random.randint(1, 10),
                random.randint(1, 10),
            )

            levels2, Dwin2 = (
                random.randint(1, 10),
                random.randint(1, 10),
            )

            with self.subTest(
                config1=(levels1, Dwin1, data1), config2=(levels2, Dwin2, data2)
            ):
                graph1 = DocumentNGramHGraph2D(
                    data1, Dwin1, levels1, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                graph2 = DocumentNGramHGraph2D(
                    data2, Dwin2, levels2, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                value = self.hpg_metric.apply(graph1, graph2)

                self.logger.debug("%s %s %4.3f", data1, data2, value)

                self.assertTrue(0.0 <= value <= 1.0)
