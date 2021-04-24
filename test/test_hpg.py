import unittest

from pyinsect.documentModel import comparators as CMP
from pyinsect.documentModel import representations as NGG


class DocumentNGramHGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.ngg1 = NGG.DocumentNGramHGraph(2, 3, 2, "abcdef")
        self.ngg2 = NGG.DocumentNGramHGraph(2, 3, 2, "abcdef")

    def test_similarity(self):
        # ngg1.GraphDraw()
        # ngg2.GraphDraw()
        gs = CMP.SimilarityNVS()

        sc = gs.getSimilarityComponents(self.ngg1, self.ngg2)
        print(sc["SS"], " ", sc["VS"])
        print(gs.getSimilarityFromComponents(sc))

        nop = CMP.LtoRNary(gs)
        print(gs.apply(self.ngg1, self.ngg2))
        bop = CMP.Union(lf=0.5, commutative=True, distributional=True)
        nop = CMP.LtoRNary(bop)

        # bop.apply(self.ngg1, self.ngg2).GraphDraw()
