from pyinsect.graphs.operators.proximity_graph_operators import BaseMergeOperator, Similarity
from pyinsect.graphs.proximity_graphs import ProximityInformation, ProximityGraph
import networkx as nx
import copy
from typing import Any

class NGGMerger(BaseMergeOperator):
    def __init__(self) -> None:
        super().__init__()

    def _update_weight(self, graph_to_update: nx.Graph, cur_edge: Any, old_weight: float, new_weight: float) -> float:
        """Updates the weight of a given edge of a specific graph, given an old and a new weight. The default implementation 
        updates using the average of the two (old and new), if the old weight is not None. Otherwise, it simply updates using
        the new value."""
        # if no old_weight assigned
        if old_weight is None:
            # Simply update with new
            graph_to_update.edges[cur_edge]['weight'] = new_weight
        else:
            # else use average
            graph_to_update.edges[cur_edge]['weight'] = (new_weight + old_weight) / 2.0

        # Return the updated weight
        return graph_to_update.edges[cur_edge]['weight']

    def merge(self, base_info: ProximityInformation, new_info: ProximityInformation, update_inline: bool, *args, **kwargs) -> ProximityInformation:
        base_info_graph = base_info.as_graph()
        new_info_graph = new_info.as_graph()

        # See if we should update inline
        if update_inline:
            # Update the base graph
            graph_to_update = base_info_graph
        else:
            # Use compose to keep the union of the nodes and edges
            graph_to_update = nx.compose(base_info_graph, new_info_graph)
            # ...and initialize weights based on base graph
            nx.set_edge_attributes(graph_to_update, base_info_graph.edges)

        # For every edge in the new info
        for cur_edge in new_info_graph.edges:
            # Read the new weight
            new_weight = new_info_graph.edges[cur_edge]['weight']
            # If edge was common
            if cur_edge in graph_to_update.edges:
                # Update it
                # by reading the old weight
                old_weight = graph_to_update.edges[cur_edge]['weight']
                # and calling the update function
                self._update_weight(graph_to_update, cur_edge, old_weight, new_weight)
            else:
                # Add the edge
                graph_to_update.add_edge(*cur_edge)
                # and initialize it through the update function
                self._update_weight(graph_to_update, cur_edge, None, new_weight)

        # Return selected graph
        return graph_to_update


