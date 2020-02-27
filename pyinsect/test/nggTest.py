import pdb
import sys
sys.path.append('..')
from pyinsect.documentModel import representations as NGG
from pyinsect.documentModel import comparators as CMP

ngg1 = NGG.DocumentNGramGraph(3,2,"abcdef")
ngg2 = NGG.DocumentNGramGraph(3,2,"abcdeff")
#ngg1.GraphDraw()
#ngg2.GraphDraw()
gs = CMP.SimilarityNVS()

sc = gs.getSimilarityComponents(ngg1,ngg2)
print((sc["SS"]," ",sc["VS"]))
print((gs.getSimilarityFromComponents(sc)))

nop = CMP.LtoRNary(gs)
print((gs.apply(ngg1,ngg2)))
bop = CMP.Union(lf=0.5, commutative=True,distributional=True)
nop = CMP.LtoRNary(bop)

bop.apply(ngg1,ngg2).GraphDraw()
