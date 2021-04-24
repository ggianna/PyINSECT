"""
   NGramCachedGraphComparator.py

 An n-gram graph similarity class
 that calculates a set of ngram graph
 similarity measures implementing
 basic similarity extraction functions.

 @author ysig
 Created on May 24, 2017, 3:56 PM
"""

from functools import reduce

from pyinsect.documentModel.comparators.Operator import BinaryOperator


# a general similarity class
# that acts as a pseudo-interface
# defining the basic class methods
class Similarity(BinaryOperator):
    def __init__(self, commutative=True, distributional=False):
        self._commutative = commutative
        self._distributional = distributional

    # given two ngram graphs
    # returns the given similarity as double
    def getSimilarityDouble(self, ngg1, ngg2):
        return 0.0

    # given two ngram graphs
    # returns some midway extracted similarity components
    # as a dictionary between of sting keys (similarity-name)
    # and double values
    def getSimilarityComponents(self, ngg1, ngg2):
        return {"SS": 0, "VS": 0, "NVS": 0}

    # from the similarity components extracts
    # what she wants for the given class
    def getSimilarityFromComponents(self, Dict):
        return 0.0

    def apply(self, *args, **kwargs):
        return self.getSimilarityDouble(*args)


class SimilaritySS(Similarity):

    # given two ngram graphs
    # returns the SS-similarity as double
    def getSimilarityDouble(self, ngg1, ngg2):
        # WRONG
        # return (min(ngg1.minW(),ngg2.minW())*1.0)/max(ngg1.maxW(),ngg2.maxW())
        y = max(ngg1.number_of_edges(), ngg2.number_of_edges())
        if y == 0:  # If both graphs are zero sized
            return 0.0  # return zero

        return (min(ngg1.number_of_edges(), ngg2.number_of_edges()) * 1.0) / max(
            ngg1.number_of_edges(), ngg2.number_of_edges()
        )

    # given two ngram graphs
    # returns the SS-similarity
    # components on a dictionary
    def getSimilarityComponents(self, ngg1, ngg2):
        return {"SS": (self.getSimilarityDouble(ngg1, ngg2))}

    # given similarity components
    # extracts the SS measure
    # if existent and returns it (as double)
    def getSimilarityFromComponents(self, Dict):
        if "SS" in Dict:
            return Dict["SS"]
        else:
            return 0.0


class SimilarityVS(Similarity):

    # given two ngram graphs
    # returns the VS-similarity as double
    def getSimilarityDouble(self, ngg1, ngg2):
        s = 0.0
        g1 = ngg1.getGraph()
        g2 = ngg2.getGraph()
        ne1 = g1.number_of_edges()
        ne2 = g2.number_of_edges()

        if ne1 == ne2 == 0:
            return 1.0

        if ne1 > ne2:
            t = g2
            g2 = g1
            g1 = t
        edges2 = set(g2.edges())  # Use set to speed up finding
        for (u, v, d) in g1.edges(data=True):
            if (u, v) in edges2:
                dp = g2.get_edge_data(u, v)
                s += min(d["weight"], dp["weight"]) / max(d["weight"], dp["weight"])
        return s / max(g1.number_of_edges(), g2.number_of_edges())

    # given two ngram graphs
    # returns the VS-similarity
    # components on a dictionary
    def getSimilarityComponents(self, ngg1, ngg2):
        return {"VS": self.getSimilarityDouble(ngg1, ngg2)}

    # given similarity components
    # extracts the SS measure
    # if existent and returns it (as double)
    def getSimilarityFromComponents(self, Dict):
        if "VS" in Dict:
            return Dict["VS"]
        else:
            return 0.0


class SimilarityNVS(Similarity):

    # given two ngram graphs
    # returns the NVS-similarity as double
    def getSimilarityDouble(self, ngg1, ngg2):
        SS = SimilaritySS()
        VS = SimilarityVS()
        return (VS.getSimilarityDouble(ngg1, ngg2) * 1.0) / SS.getSimilarityDouble(
            ngg1, ngg2
        )

    # given two ngram graphs
    # returns the NVS-similarity
    # components e.g. SS and VS
    # on a dictionary
    def getSimilarityComponents(self, ngg1, ngg2):
        SS = SimilaritySS()
        VS = SimilarityVS()
        return {
            "SS": SS.getSimilarityDouble(ngg1, ngg2),
            "VS": VS.getSimilarityDouble(ngg1, ngg2),
        }

    # given a dictionary containing
    # SS similarity and VS similarity
    # extracts NVS if SS is not 0
    def getSimilarityFromComponents(self, Dict):
        if ("SS" in Dict and "VS" in Dict) and (str(Dict["SS"]) != "0.0"):
            return (Dict["VS"] * 1.0) / Dict["SS"]
        else:
            return 0.0


class SimilarityVSHPG(SimilarityVS):
    def getSimilarityDouble(self, ngg1, ngg2):
        ngg2_levels = ngg2.subgraphs + [ngg2]
        ngg1_levels = ngg1.subgraphs + [ngg1]

        rv = 0
        for level, (subngg1, subngg2) in enumerate(zip(ngg1_levels, ngg2_levels)):
            similarity = super().getSimilarityDouble(subngg1, subngg2)
            rv += (level + 1) * similarity

        return rv / reduce(lambda x, y: x + y, range(1, level + 2))
