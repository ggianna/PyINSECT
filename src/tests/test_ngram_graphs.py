import sys, os
import networkx as nx
import matplotlib.pyplot as plt
import logging as log
from typing import Any

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
import pyinsect.graphs.operators.proximity_graph_operators as pgops


def test_ngram_graph_creation():
    def draw_graph_with_weights(g_to_draw : ProximityGraph, output_dot_file : str = "/tmp/mygraph.dot"):
        # Clear figure
        plt.clf()
        # Save to file
        temp_ag = nx.nx_agraph.to_agraph(g_to_draw)
        temp_ag.write("/tmp/mygraph.dot")    
        #Also output parameters
        print(f"Graph class: {g_to_draw.__class__}; String: {g_to_draw.data}; Parameters: (n: {my_graph.n}, DWin: {my_graph.Dwin})")
        # And graph to console
        print("Content:", temp_ag.to_string())

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


def test_ngram_graph_comparison():
    def output_similarity(simop : pgops.BaseSimilarityOperator, to_print: pgops.Similarity, obj1name : str = "Obj1", obj2name : str = "Obj2"):
        print(f"+++ Reference object name: {obj1name}; Evaluated object name: {obj2name};\nSimilarity type: {simop.__class__}; Value: {to_print.value}; Components: {to_print.components}")

    def output_variations(simop : pgops.BaseSimilarityOperator, ag1, ag2, agIrr, data1, data2, dataIrr):
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
        for simop_class in [pgops.SizeSimilarity, pgops.SymmetricContainmentSimilarity, pgops.AsymmetricContainmentSimilarity, 
            pgops.SymmetricValueSimilarity, pgops.AsymmetricValueSimilarity]:
            log.info(f"+++ +++Examining similarity {str(simop_class)}...")
            simop = simop_class()

            output_variations(simop, ag1, ag2, agIrr, data1, data2, dataIrr)

        log.info(f"--- Tests for class {str(cur_class)}... Done.")

    log.info("Symmetric tests... Done.")


def main():
    test_ngram_graph_creation()
    test_ngram_graph_comparison()

if __name__ == "__main__":
    main()