"""
   NGramCachedGraphComparator.py

 An n-gram graph similarity class
 that calculates a set of ngram graph
 similarity measures implementing
 basic similarity extraction functions.

 @author ysig
 Created on May 24, 2017, 3:56 PM
"""

import logging

from pyinsect.documentModel.comparators.Operator import BinaryOperator

logger = logging.getLogger(__name__)

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

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)


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

        try:
            return (VS.getSimilarityDouble(ngg1, ngg2) * 1.0) / SS.getSimilarityDouble(
                ngg1, ngg2
            )
        except ZeroDivisionError:
            return 0.0

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


class SimilarityHPG(Similarity):
    """A custom `Similarity` metric tailored to the complexities
    of Hierarchical Proximity Graphs (`HPG`).

    Given two HPGs, the `Value Similarity` of every sub-graph pair is computed,
    on a pair level basis, and the weighted mean of among all levels is considered
    the HPGs Value Similarity.
    """

    def __init__(self, per_level_similarity_metric):
        super().__init__()

        self._per_level_similarity_metric = per_level_similarity_metric

    def getSimilarityDouble(self, document_n_gram_h_graph1, document_n_gram_h_graph2):
        if not document_n_gram_h_graph1 and not document_n_gram_h_graph2:
            logger.debug(
                "Both %s and %s graphs are empty",
                document_n_gram_h_graph1,
                document_n_gram_h_graph2,
            )
            return 1

        if not document_n_gram_h_graph1 or not document_n_gram_h_graph2:
            logger.debug(
                "One of %s and %s graphs are empty",
                document_n_gram_h_graph1,
                document_n_gram_h_graph2,
            )
            return 0

        lvls, similarity = [], 0

        for lvl, (current_1, current_2) in enumerate(
            zip(document_n_gram_h_graph1, document_n_gram_h_graph2), start=1
        ):
            logger.debug(
                "Calculating similarity of graphs %s and %s on level %02d",
                current_1,
                current_2,
                lvl,
            )

            if not current_1 and not current_2:
                # NOTE: In the context a multi-level HPG, it is highly probable that,
                # one or more sub-graph might degenerate to empty graphs.
                # Given a similarity metric such as `SimilarityNVS`,
                # this would entail, that the similarity of two identical HPGs,
                # containing empty sub-graphs would not receive the expected
                # value of 1.
                # For the time being, such degenerate sub-graphs are going
                # to be completely ignored when calculating the similarity of
                # 2 HPGs.
                # For example, given 2 5 level HPGs, if levels 4 and 5 are empty
                # and every other corresponding sub-graphs of the two are identical
                # the HPG similarity of the two is going to be calculated as such
                # `(1 * 1 + 1 * 2 + 1 * 3) / (1 + 2 + 3)`
                # instead of
                # `(1 * 1 + 1 * 2 + 1 * 3 + 0 * 4 + 0 * 5) / (1 + 2 + 3 + 4 + 5)`
                logger.debug("Both %s and %s graphs are empty", current_1, current_2)
                continue

            current_lvl_similarity = (
                self._per_level_similarity_metric.getSimilarityDouble(
                    current_1, current_2
                )
            )

            logger.debug(
                "The similarity of graphs %s and %s is %05.3f",
                current_1,
                current_2,
                current_lvl_similarity,
            )

            similarity += lvl * current_lvl_similarity

            logger.debug(
                "The overall similarity of graph %s and graph %s is %05.3f",
                document_n_gram_h_graph1,
                document_n_gram_h_graph2,
                (similarity / sum(lvls)) if lvls else 0,
            )

            lvls.append(lvl)

        return similarity / sum(lvls) if lvls else 0
