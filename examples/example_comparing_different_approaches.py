from pyinsect.documentModel import representations as NGG

if __name__ == "__main__":
    n = 3
    Dwin = 2
    text = "GATTACATTAG"

    ngg = NGG.DocumentNGramGraph(n, Dwin, text)
    ngg.GraphDraw()

    ngswg = NGG.DocumentNGramSymWinGraph(n, Dwin, text)
    ngswg.GraphDraw()

    nggng = NGG.DocumentNGramGaussNormGraph(n, Dwin, text)
    nggng.GraphDraw()
