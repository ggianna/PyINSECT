import sys, os
import networkx as nx
import matplotlib.pyplot as plt
import logging as log
from typing import Any
from copy import deepcopy

# Verbose logging
log.basicConfig(level=log.INFO)

# Add module to search path
sDir = os.path.dirname(__file__) + "/.."
print(f"Adding {sDir} to search path...")
sys.path.insert(0, sDir)

# Init logging
import pyinsect.utils.logging

# Import classes
from pyinsect.graphs.ngram_graphs import (AsymmetricNGramGraph, SymmetricNGramGraph, ProximityGraph)
import pyinsect.graphs.operators.ngg_similarity_operators as nggsimops
import pyinsect.graphs.operators.ngg_merging_operators as nggsmergeops

def draw_graph_with_weights(g_to_draw : ProximityGraph, output_dot_file : str = "/tmp/mygraph.dot", draw_to_figure: bool = False):
    # Save to file
    temp_ag = nx.nx_agraph.to_agraph(g_to_draw)
    temp_ag.write("/tmp/mygraph.dot")    
    #Also output parameters
    print(f"Graph class: {g_to_draw.__class__}; String: {g_to_draw.data}; Parameters: (n: {g_to_draw.n}, DWin: {g_to_draw.Dwin})")
    # And graph to console
    print("Content:", temp_ag.to_string())

    if draw_to_figure:
        # Clear figure
        plt.clf()
        # Create labels
        edge_labels = {n: g_to_draw.edges[n]['weight'] for n in g_to_draw.edges}
        node_labels = {n: n for n in g_to_draw.nodes}
        # Layout
        pos = nx.nx_agraph.graphviz_layout(g_to_draw)
        # Actually draw network
        nx.draw(g_to_draw, pos=pos, with_labels=True, labels = node_labels)
        # Add edges with labels
        nx.draw_networkx_edge_labels(g_to_draw, pos=pos, edge_labels=edge_labels)
        # Show figure
        plt.show()


def test_ngram_graph_creation():

    my_str = "1234567"
    # Asymmetric tests
    log.info("Asymmetric graph tests...")
    my_graph = AsymmetricNGramGraph(data=my_str)
    draw_graph_with_weights(my_graph)

    my_graph = AsymmetricNGramGraph(data=my_str, n=1, Dwin=2)
    draw_graph_with_weights(my_graph)

    my_graph = AsymmetricNGramGraph(data=my_str, n=2, Dwin=1)
    draw_graph_with_weights(my_graph)

    my_graph = AsymmetricNGramGraph(data=my_str, n=3, Dwin=10)
    draw_graph_with_weights(my_graph)

    my_graph = AsymmetricNGramGraph(data=my_str, n=10, Dwin=3)
    draw_graph_with_weights(my_graph)
    log.info("Asymmetric graph tests... Done.")

    # Symmetric tests
    log.info("Symmetric graph tests...")
    my_graph = SymmetricNGramGraph(data=my_str)
    draw_graph_with_weights(my_graph)

    my_graph = SymmetricNGramGraph(data=my_str, n=1, Dwin=2)
    draw_graph_with_weights(my_graph)

    my_graph = SymmetricNGramGraph(data=my_str, n=2, Dwin=1)
    draw_graph_with_weights(my_graph)

    my_graph = SymmetricNGramGraph(data=my_str, n=3, Dwin=10)
    draw_graph_with_weights(my_graph)

    my_graph = SymmetricNGramGraph(data=my_str, n=10, Dwin=3)
    draw_graph_with_weights(my_graph)
    log.info("Symmetric graph tests... Done.")

    log.info("Merging tests...")


def test_ngram_graph_comparison():
    def output_similarity(simop : nggsimops.BaseSimilarityOperator, to_print: nggsimops.Similarity, obj1name : str = "Obj1", obj2name : str = "Obj2"):
        print(f"+++ Reference object name: {obj1name}; Evaluated object name: {obj2name};\nSimilarity type: {simop.__class__}; Value: {to_print.value}; Components: {to_print.components}")

    def output_variations(simop : nggsimops.BaseSimilarityOperator, ag1, ag2, agIrr, data1, data2, dataIrr):
        # Different overlapping
        output_similarity(simop, simop.similarity(ag1, ag2), data1, data2)
        # Reversed different overlapping
        output_similarity(simop, simop.similarity(ag2, ag1), data2, data1)
        # Irrelevant
        output_similarity(simop, simop.similarity(ag1, ag1), data2, data1)
        # Self-similarity
        output_similarity(simop, simop.similarity(ag1, agIrr), data1, dataIrr)
    
    # Init strings
    data1 = "123456"
    data2 = "3456789345456"
    dataIrr = "hello world!"

    # For each graph type
    for cur_class in [AsymmetricNGramGraph, SymmetricNGramGraph]:
        log.info(f"+++ Tests for graph class {str(cur_class)}...")
        ag1 = cur_class(data=data1)
        ag2 = cur_class(data=data2)
        agIrr = cur_class(data=dataIrr)

        # For each similarity type
        for simop_class in [nggsimops.SizeSimilarity, nggsimops.SymmetricContainmentSimilarity, nggsimops.AsymmetricContainmentSimilarity, 
            nggsimops.SymmetricValueSimilarity, nggsimops.AsymmetricValueSimilarity]:
            log.info(f"+++ +++Examining similarity {str(simop_class)}...")
            simop = simop_class()

            output_variations(simop, ag1, ag2, agIrr, data1, data2, dataIrr)

        log.info(f"--- Tests for class {str(cur_class)}... Done.")

    log.info("Symmetric tests... Done.")

def test_ngram_graph_merging():
    log.info("Merging tests...")
    # Init strings
    data1 = "abcdef"
    data2 = "cdefghijcdef"
    dataIrr = "hello world!"

    def output_merged_graph(merger : nggsmergeops.BaseMergeOperator, to_merge1: ProximityGraph, to_merge2: ProximityGraph, inline_merge: bool,
                                graph1_description : str = "Graph1", graph2_description : str = "Graph2"):

        # Perform the merging
        merged_graph = merger.merge(to_merge1, to_merge2, inline_merge)
        similarity_to_base = nggsimops.SymmetricValueSimilarity().similarity(to_merge1, merged_graph)

        print(f"+++ Reference graph name: {graph1_description}; New graph name: {graph2_description}; Inline: {inline_merge};\n" + \
                f"Merger type: {merger.__class__}; Similarity between reference and merged: {similarity_to_base}.\n" + \
                f"Content:\n {    nx.nx_agraph.to_agraph(merged_graph.as_graph()).to_string()}"
                )

    def output_variations(mergeop : nggsmergeops, ag1, ag2, agIrr, data1, data2, dataIrr):
        # For inline and not inline
        for inline in [True, False]:
            # Different overlapping
            output_merged_graph(mergeop, deepcopy(ag1), deepcopy(ag2), inline, data1, data2)

            # Reversed different overlapping
            output_merged_graph(mergeop, deepcopy(ag2), deepcopy(ag1), inline, data2, data1)

            # Irrelevant
            output_merged_graph(mergeop, deepcopy(ag1), deepcopy(agIrr), inline, data1, dataIrr)

            # Self-similarity
            output_merged_graph(mergeop, deepcopy(ag1), deepcopy(ag1), inline, data1, data1)
            

    # For each graph type
    for cur_class in [AsymmetricNGramGraph, SymmetricNGramGraph]:
        log.info(f"+++ Tests for graph class {str(cur_class)}...")
        ag1 = cur_class(data=data1)
        ag2 = cur_class(data=data2)
        agIrr = cur_class(data=dataIrr)

        # For each merging type
        for mergeop_class in [nggsmergeops.NGGMerger]:
            log.info(f"+++ +++Examining merging operator {str(mergeop_class)}...")
            mergeop = mergeop_class()

            output_variations(mergeop, ag1, ag2, agIrr, data1, data2, dataIrr)

        log.info(f"--- Tests for class {str(cur_class)}... Done.")

    log.info("Merging tests... Done.")


def main():
    test_ngram_graph_creation()
    test_ngram_graph_comparison()
    test_ngram_graph_merging()

if __name__ == "__main__":
    main()