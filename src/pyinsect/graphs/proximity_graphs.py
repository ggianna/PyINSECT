from networkx import DiGraph, Graph
from abc import *
from collections.abc import Iterable, Iterator
from typing import Callable, Any, List, Dict
import numpy as np
import networkx as nx

# ALWAYS init logging
import pyinsect.utils.logging
import logging as log
#####################

# TODO: Deal with access to specific items of a partition, probably as another class or partition indexing.

class PartitionableObject(ABC):
    pass

class Partitioner(ABC):
    """A class that can partition partitionable objects."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
    
    @abstractmethod
    def partition(self, to_partition: PartitionableObject) -> Iterable:
        raise NotImplementedError("Partitioning function not implemented.")


class ProximityInformation(ABC):
    """A graph that represents statistics of proximity of items. """

    def as_graph(self) -> Graph:
        """Returns a graph representation of the proximity information. Edges are expected to represent items that can be found in proximity of
        each other, while the edge data, e.g. weight (if any), provides information on the proximity."""
        
        raise NotImplementedError("Graph representation not implemented for ProximityInformation.")

    def as_matrix(self) -> np.array:
        """Returns a graph representation of the proximity information.  Rows and columns are expected to be mapped to items that can be found in 
        proximity of each other, while the matrix cell/positions data provides information on the proximity. """
        
        raise NotImplementedError("Matrix representation not implemented for ProximityInformation.")

    def as_dict(self) ->  Dict[Dict, Dict]:
        """Returns a dictionary representation of the proximity information. Typically each key represents a pair of items which can be found in proximity
        of one another. The corresponding proximity is represented in the value mapped to the key."""
        
        raise NotImplementedError("Dictionary representation not implemented for ProximityInformation.")

    
class ProximityGraph(ProximityInformation, Graph):
    """A graph that represents the statistics of proximity, typically ignoring directionality (i.e. not
    differentiating between the proximity of A to B and vice versa). This handling of directionality can be changed
    in subclasses."""
    
    def __init__(self, *attr, data = None, **kwargs):
        """Creates a proximity graph, which represents proximity information."""
        ProximityInformation.__init__(self)
        Graph.__init__(self, *attr, **kwargs)
        self.data = data

    def as_graph(self) -> Graph:
        return self
    
    def as_matrix(self) -> np.array:
        return nx.to_numpy_array(self)

    def as_dict(self) -> Dict[Dict, Dict]:
        return nx.to_dict_of_dicts(self)


class ProximityDiGraph(DiGraph, ProximityInformation):
    """A graph that represents the statistics of proximity of paritions in a partitionable object, especially noting directionality 
    (i.e. explicitly differentiating between the proximity of A to B and vice versa)."""

    def __init__(self, *attr, **kwargs):
        """Creates an proximity graph, taking into account directionality."""

        ProximityInformation.__init__(self)
        DiGraph.__init__(self, attr, kwargs)


    def as_graph(self) -> DiGraph:
        return self
    
    def as_matrix(self) -> np.array:
        return nx.to_numpy_array(self)

    def as_dict(self) -> Dict[Dict, Dict]:
        return nx.to_dict_of_dicts(self)
