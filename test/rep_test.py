import sys
sys.path.append('..')
from pyinsect.documentModel import representations as NGG

# a test for the family of ngrams

n = 3
Dwin = 2
text = "GATTACATTAG"

ngg = NGG.DocumentNGramGraph(n,Dwin,text)
ngg.GraphDraw()

ngswg = NGG.DocumentNGramSymWinGraph(n,Dwin,text)
ngswg.GraphDraw()

nggng = NGG.DocumentNGramGaussNormGraph(n,Dwin,text)
nggng.GraphDraw()
