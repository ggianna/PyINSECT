#!/usr/bin/python
import pdb
from documentModel import *

"""
 An n-gram graph collector, which can create representative graphs of text/graph sets
 and can calculate appropriateness (essentially the similarity) of a text, with respect 
 to the representative graph.
 
 @author ggianna
"""
class NGramGraphCollector:
    def __init__(self):
        self._iDocs = 0.0
        self._gOverallGraph = None
    
    """
        Adds the graph of the input text to the representative graph.
    """
    def addText(self, sText, bDeepCopy=False, n = 3, Dwin = 3):
        ngg1 = DocumentNGramGraph(n,Dwin,sText)
        self.addGraph(ngg1, bDeepCopy)

        
    """
        Adds the graph input to the representative graph.
    """
    def addGraph(self, gNewGraph, bDeepCopy=False):  # Do NOT use deep copy by default
        if (self._iDocs == 0):
            self._gOverallGraph = gNewGraph
        else:
            bop = Union(lf=1.0 / (self._iDocs + 1.0), commutative=True,distributional=True)
            self._gOverallGraph = bop.apply(self._gOverallGraph, gNewGraph, dc=bDeepCopy)
        # Added a doc
        self._iDocs += 1
    
    """
        Returns a degree of ''appropriateness'' of a text, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the text to the representative graph.
    """
    def getAppropriateness(self, sText, n = 3, Dwin = 3):
        nggNew = DocumentNGramGraph(n,Dwin,sText)
        gs = SimilarityNVS()
        return gs.getSimilarityDouble(nggNew, self._gOverallGraph)

    """
        Returns a degree of ''appropriateness'' of a graph, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the graph to the representative graph.
    """
    def getGraphAppropriateness(self, gGraph):
        gs = SimilarityNVS()
        return gs.getSimilarityDouble(gGraph, self._gOverallGraph)

    """
     Returns the representative graph of the collection input.
    """
    def getRepresentativeGraph(self):
        return self._gOverallGraph




if __name__ == "__main__":
    import random;
    import time;


    def getRandomText(iSize):
        # lCands = list("abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper() + "1234567890!@#$%^&*()")
        lCands = list("abcdef")
        sRes = "".join([ random.choice(lCands) for i in range(1,iSize) ])
        return sRes


    # Start test
    import time

    print "Initializing texts..."
    lTexts = list()
    for iCnt in range(0,50):
        # Select text size
        iSize = random.randint(1000,2000);
        sText = getRandomText(iSize)
        # Add to list
        lTexts.append(sText)
    print "Initializing texts... Done."


    print "Starting shallow..."
    cNoDeep = NGramGraphCollector()
    start = time.time()
    lastStep = start
    # No deep
    iCnt = 0
    for sText in lTexts:
        cNoDeep.addText(sText)
        iCnt += 1
        if (time.time() - lastStep > 1):
            print "..." + str(iCnt)
            lastStep = time.time()

    end = time.time()
    print(end - start)
    print "End shallow."

    # print "Starting deep..."
    # cDeep = NGramGraphCollector()
    # start = time.time()
    # # Deep
    # for sText in lTexts:
    #     cDeep.addText(sText, True)
    #     if (time.time() - lastStep > 1):
    #         print "."
    #         lastStep = time.time()
    # end = time.time()
    # print(end - start)
    # print "End deep."
