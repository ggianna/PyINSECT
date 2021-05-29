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

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=logging.DEBUG,
)


class DocumentNGramHGraphTestCase(unittest.TestCase):
    def setUp(self):
        random.seed(1234)

        self.data = self.generate_random_2d_int_array(5)

        self.array_graph_metric = SimilarityVS()
        self.hpg_metric = SimilarityHPG(self.array_graph_metric)

    def test_same_similarity(self):
        graph1 = DocumentNGramHGraph2D(
            self.data, 3, 3, self.array_graph_metric
        ).as_graph(DocumentNGramGraph)

        graph2 = DocumentNGramHGraph2D(
            self.data, 3, 3, self.array_graph_metric
        ).as_graph(DocumentNGramGraph)

        value = self.hpg_metric(graph1, graph2)

        self.assertEqual(value, 1.0)

    def test_diff_similarity(self):
        for permutation_index, permutation in enumerate(
            itertools.permutations(self.data)
        ):
            if permutation == tuple(self.data):
                continue

            logger.info("Permutation: %02d", permutation_index)

            with self.subTest(permutation=permutation):
                graph1 = DocumentNGramHGraph2D(
                    permutation, 3, 3, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                graph2 = DocumentNGramHGraph2D(
                    self.data, 3, 3, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                value = self.hpg_metric(graph1, graph2)

                self.assertNotEqual(value, 1.0)

    def test_commutativity(self):
        data1 = self.generate_random_2d_int_array(5)
        data2 = self.generate_random_2d_int_array(5)

        graph1 = DocumentNGramHGraph2D(data1, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        graph2 = DocumentNGramHGraph2D(data2, 3, 3, self.array_graph_metric).as_graph(
            DocumentNGramGraph
        )

        value1 = self.hpg_metric(graph1, graph2)
        value2 = self.hpg_metric(graph2, graph1)

        self.assertEqual(value1, value2)

    def test_combinations(self):
        for combination_index in range(10):
            logger.info("Combination: %02d", combination_index)

            length1 = random.randint(1, 5)
            length2 = random.randint(1, 5)

            data1 = self.generate_random_2d_int_array(length1)
            data2 = self.generate_random_2d_int_array(length2)

            levels1, Dwin1 = (
                random.randint(1, 4),
                random.randint(1, 10),
            )

            levels2, Dwin2 = (
                random.randint(1, 4),
                random.randint(1, 10),
            )

            logger.info("Configuration #1: (%02d, %02d)", levels1, Dwin1)
            logger.info("Configuration #2: (%02d, %02d)", levels2, Dwin2)

            with self.subTest(
                config1=(levels1, Dwin1, data1), config2=(levels2, Dwin2, data2)
            ):
                graph1 = DocumentNGramHGraph2D(
                    data1, Dwin1, levels1, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                graph2 = DocumentNGramHGraph2D(
                    data2, Dwin2, levels2, self.array_graph_metric
                ).as_graph(DocumentNGramGraph)

                value = self.hpg_metric(graph1, graph2)

                self.assertTrue(0.0 <= value <= 1.0)

    @classmethod
    def generate_random_2d_int_array(cls, size):
        return [
            [ord(random.choice(string.ascii_letters)) for _ in range(size)]
            for _ in range(size)
        ]
