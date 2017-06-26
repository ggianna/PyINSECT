import sys
sys.path.append('..')
from source import representations as NGG

ngg = NGG.DocumentNGramGraph(3,2,"abcdef")
ngg.GraphDraw()

ngswg = NGG.DocumentNGramSymWinGraph(3,4,"abcdef")
ngswg.GraphDraw()

nggng = NGG.DocumentNGramGaussNormGraph(3,4,"abcdefg")
nggng.GraphDraw()
