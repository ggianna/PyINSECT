#!/usr/bin/env python

"""
 * DocumentNGramGraph.java
 *
 * Created on 17/5/2017 16:00
 *
"""

import logging

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.isomorphism import numerical_edge_match
from networkx.drawing.nx_agraph import graphviz_layout

logger = logging.getLogger(__name__)

"""
 *  Represents the graph of a document, with vertices n-grams of the document and edges the number
 * of the n-grams' co-occurences within a given window.
 #*
 * @author ysig
"""


class DocumentNGramGraph:
    # initialization
    def __init__(self, n=3, Dwin=2, Data=[], GPrintVerbose=True):
        # consider not having characters but lists of objects
        self._Data = []

        # data size build for reuse of len(data)
        self._dSize = 0

        # stores the ngram
        self._ngram = []

        # store the ngram graph
        self._Graph = nx.DiGraph()

        # cache of edges (set vs. list)
        self._edges = set()

        # the graph stores it's maximum and minimum weigh
        self._maxW = 0
        self._minW = float("inf")

        # data must be "listable"
        self._Dwin = abs(int(Dwin))
        # n for the n-graph
        self._n = abs(int(n))
        self.setData(Data)
        # a printing flag determining if the printing result will be stored on document or
        # be displayed on string
        self._GPrintVerbose = GPrintVerbose
        if not (self._Data == []):
            self.buildGraph()

    def __len__(self):
        return self._Graph.size()

    def __eq__(self, other):
        return nx.is_isomorphic(
            self._Graph, other._Graph, edge_match=numerical_edge_match("weight", 1)
        )

    # we will now define @method buildGraph
    # which takes a data input
    # segments ngrams
    # and creates ngrams based on a given window
    # !notice: at this developmental stage the weighting method
    # may not be correct
    def buildGraph(self, verbose=False, d=[]):
        # set Data @class_var
        self.setData(d)
        self._Data

        # build ngram
        ng = self.build_ngram()
        s = len(ng)

        self._Dwin

        # init graph
        # TODO: add clear function

        o = min(self._Dwin, s)
        if o >= 1:
            window = [ng[0]]
            # append the first full window
            # while adding the needed edges
            for gram in ng[1 : o + 1]:
                for w in window:
                    self.addEdgeInc(gram, w)
                window.append(gram)

            # with full window span till
            # the end.
            for gram in ng[o + 1 :]:
                for w in window:
                    self.addEdgeInc(gram, w)
                window.pop(0)
                window.append(gram)

            # print graph (optional)
            if verbose:
                self.GraphDraw(self._GPrintVerbose)
        return self._Graph

    # add's an edge if it's non existent
    # if it is increments it's weight
    # !notice: reiweighting technique may be false
    # at this developmental stage
    def addEdgeInc(self, a, b, w=1):
        # A = repr(a)#str(a)
        # B = repr(b)#str(b)
        # merging can also be done in other ways
        # add an extra class variable
        A = tuple(a)
        B = tuple(b)
        if (A, B) in self._edges:
            edata = self._Graph.get_edge_data(A, B)
            # DEBUG LINES
            # print "updating edge between (",A,B,")"
            # print "to weight",(edata['weight']+1)

            r = edata["weight"] + w
        else:
            # DEBUG LINES
            # print "adding edge between (",A,B,")"

            r = w
        # update/add edge weight
        self.setEdge(A, B, r)

    # creates ngram's of window based on @param n
    def build_ngram(self, d=[]):
        self.setData(d)
        Data = self._Data
        l = Data[0 : min(self._n, self._dSize)]
        q = []
        q.append(l[:])
        if self._n < self._dSize:
            for d in Data[min(self._n, self._dSize) :]:
                l.pop(0)
                l.append(d)
                q.append(l[:])
        self._ngram = q
        return q

    # draws a graph using math plot lib
    def GraphDraw(self, verbose=True, print_name="graph", lf=True, ns=1000, wf=True):
        pos = graphviz_layout(self._Graph)
        # pos = sring_layout(self._Graph, scale=1)
        # nx.draw(self._Graph,pos = pos,node_size=ns,with_labels = lf, node_color = 'm')
        nx.draw(
            self._Graph,
            pos=graphviz_layout(self._Graph, prog="dot"),
            node_size=ns,
            cmap=plt.cm.Blues,
            node_color=list(range(len(self._Graph))),
            with_labels=lf,
        )
        if wf:
            weight_labels = nx.get_edge_attributes(self._Graph, "weight")
            nx.draw_networkx_edge_labels(
                self._Graph, pos=pos, edge_labels=weight_labels
            )
        if verbose:
            plt.show()
        else:
            # plt.savefig('g.png')
            # or to dot
            nx.drawing.nx_pydot.write_dot(self._Graph, print_name + ".dot")
            # !!Uknown error: the produced dot file is
            # not readable by dot/xdot.

    ## set functions for structure's protected fields

    def setData(self, Data):
        if not (Data == []):
            self._Data = list(Data)
            self._dSize = len(self._Data)

    # sets an edges weight
    def setEdge(self, a, b, w=1):
        self._edges.add((a, b))  # Update cache
        self._Graph.add_edge(a, b, key="edge", weight=w)

        self._maxW = max(self._maxW, w)
        self._minW = min(self._minW, w)

    # deletes
    def delEdge(self, u, v):
        self._edges.remove((u, v))
        self._Graph.remove_edge(u, v)

    # trims the graph by removing unreached nodes
    def deleteUnreachedNodes(self):
        self._Graph.remove_nodes_from(list(nx.isolates(self._Graph)))

    def setN(self, n):
        self._n = n

    def setDwin(self, win):
        self._Dwin = win

    ## get functions for structures protected fields
    def getMin(self):
        return self._MinSize

    def getngram(self):
        return self._ngram

    def getGraph(self):
        return self._Graph

    def maxW(self):
        return self._maxW

    def minW(self):
        return self._minW

    def number_of_edges(self):
        return self._Graph.number_of_nodes()

    def union(self, other, learning_factor=0.5):
        """

        Pseudocode:

            For graphs G1,G2 where smallGraph = min(G1,G2) & bigGraph = max(G1,G2)
            bigGraph gets deepcopied to `bigGraph`
            For all (A,B) belongs in smallGraph edges
            if (A,B) belongs also to bigGraph edges (deep-copied graph)
                replace the weight with value w1*lf+w2*(1-lf) on `bigGraph`
            else
                add edge to `bigGraph` with the value it has on small graph
            return `bigGraph`
        """

        other_graph = other.getGraph()

        # Convert edge-list to set to speed-up look-up
        edge_set = set(self._Graph.edges())

        for (vertex_start, vertex_end, edge_data) in other_graph.edges(data=True):
            edge_weight = edge_data["weight"]

            if (vertex_start, vertex_end) in edge_set:
                current_edge_data = self._Graph.get_edge_data(vertex_start, vertex_end)
                current_edge_weight = current_edge_data["weight"]

                edge_weight = (
                    learning_factor * edge_weight
                    + (1 - learning_factor) * current_edge_weight
                )

            self.setEdge(vertex_start, vertex_end, edge_weight)

        return self


# test script

# 1. construct a 2-gram graph of window_size = 2
#   from the word "abcdef"
