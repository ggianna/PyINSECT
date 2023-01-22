import sys, os
from networkx.readwrite import json_graph
import json
import networkx as nx
import matplotlib.pyplot as plt
import logging as log


# Add module to search path
sDir = os.path.dirname(__file__) + "/.."
print(f"Adding {sDir} to search path...")
sys.path.insert(0, sDir)

# Init logging
import pyinsect.utils.logging as pyi_log
pyi_log.init_logging(level=log.INFO)

# Import classes
from pyinsect.graphs.ngram_graphs import (AsymmetricNGramGraph, SymmetricNGramGraph, ProximityGraph)


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
    log.log(log.INFO, "Asymmetric tests...")
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
    log.log(log.INFO, "Asymmetric tests... Done.")

    # Symmetric tests
    log.log(log.INFO, "Symmetric tests...")
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
    log.log(log.INFO, "Symmetric tests... Done.")


def test_ngram_graph_comparison():
    ag1 = AsymmetricNGramGraph()


def main():
    test_ngram_graph_creation()
    test_ngram_graph_comparison()

if __name__ == "__main__":
    main()