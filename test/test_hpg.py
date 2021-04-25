import itertools
import random
import string
import unittest

from pyinsect.documentModel import comparators as CMP
from pyinsect.documentModel import representations as NGG


class DocumentNGramHGraphTestCase(unittest.TestCase):
    def setUp(self):
        random.seed(1234)

        self.text = "abcdef"

        self.metric = CMP.SimilarityVSHPG()

    def test_same_similarity(self):
        ngg1 = NGG.DocumentNGramHGraph(2, 3, 2, self.text)
        ngg2 = NGG.DocumentNGramHGraph(2, 3, 2, self.text)

        value = self.metric.apply(ngg1, ngg2)

        self.assertEqual(value, 1.0)

    def test_diff_similarity(self):
        for permutation in itertools.permutations(self.text):
            if permutation == tuple(self.text):
                continue

            with self.subTest(permutation=permutation):
                ngg1 = NGG.DocumentNGramHGraph(2, 3, 2, permutation)
                ngg2 = NGG.DocumentNGramHGraph(2, 3, 2, self.text)

                value = self.metric.apply(ngg1, ngg2)

                self.assertNotEqual(value, 1.0)

    def test_commutativity(self):
        length1 = random.randint(1, len(string.ascii_letters))
        length2 = random.randint(1, len(string.ascii_letters))

        text1 = "".join(random.choice(string.ascii_letters) for _ in range(length1))
        text2 = "".join(random.choice(string.ascii_letters) for _ in range(length2))

        ngg1 = NGG.DocumentNGramHGraph(2, 3, 2, text1)
        ngg2 = NGG.DocumentNGramHGraph(2, 3, 2, text2)

        value1 = self.metric.apply(ngg1, ngg2)
        value2 = self.metric.apply(ngg2, ngg1)

        self.assertEqual(value1, value2)

    def test_combinations(self):
        for _ in range(10):
            length1 = random.randint(1, len(string.ascii_letters))
            length2 = random.randint(1, len(string.ascii_letters))

            text1 = "".join(random.choice(string.ascii_letters) for _ in range(length1))
            text2 = "".join(random.choice(string.ascii_letters) for _ in range(length2))

            levels1, n1, Dwin1 = (
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10),
            )
            levels2, n2, Dwin2 = (
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10),
            )

            with self.subTest(
                config1=(levels1, n1, Dwin1, text1), config2=(levels2, n2, Dwin2, text2)
            ):
                ngg1 = NGG.DocumentNGramHGraph(levels1, n1, Dwin1, text1)
                ngg2 = NGG.DocumentNGramHGraph(levels2, n2, Dwin2, text2)

                value = self.metric.apply(ngg1, ngg2)

                self.assertTrue(0.0 <= value <= 1.0)
