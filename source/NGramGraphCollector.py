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
    def addText(self, sText):
        ngg1 = DocumentNGramGraph(3,3,sText)
        self.addGraph(ngg1)

        
    """
        Adds the graph input to the representative graph.
    """
    def addGraph(self, gNewGraph):
        if (self._iDocs == 0):
            self._gOverallGraph = gNewGraph
        else:
            bop = Union(lf=1.0 / (self._iDocs + 1.0), commutative=True,distributional=True)
            self._gOverallGraph = bop.apply(self._gOverallGraph, gNewGraph)
        # Added a doc
        self._iDocs += 1
    
    """
        Returns a degree of ''appropriateness'' of a text, given the representative graph.
        Essentially it calculates the Normalized Value Similarity of the text to the representative graph.
    """
    def getAppropriateness(self, sText):
        nggNew = DocumentNGramGraph(3,3,sText)
        gs = SimilarityNVS()
        return gs.getSimilarityDouble(nggNew, self._gOverallGraph)