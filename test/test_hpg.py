import unittest

from pyinsect.documentModel import comparators as CMP
from pyinsect.documentModel import representations as NGG


class DocumentNGramHGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.ngg1 = NGG.DocumentNGramHGraph(2, 3, 2, "abcdef")
        self.ngg2 = NGG.DocumentNGramHGraph(2, 3, 2, "abcdef")

    def test_similarity(self):
        smlr = CMP.SimilarityVSHPG()

        value = smlr.apply(self.ngg1, self.ngg2)

        self.assertEqual(value, 1)
