from pyinsect.graphs.proximity_graphs import *

class PartitionableString(str, PartitionableObject):
    def __init__(self, partitioner : Partitioner) -> None:
        str.__init__(self)
        PartitionableObject.__init__(self)

class TextNGramPartitioner(Partitioner):
    def __init__(self, ngram_size: int, pad_string : bool = False) -> None:
        super().__init__()

        if ngram_size < 1:
            raise ValueError("Ngram size cannot be less than 1.")

        self.ngram_size = ngram_size
        self.pad_string = pad_string

    
    def partition(self, to_partition: PartitionableString) -> Iterable:
        """A generator returning the list of overlapping n-grams in the string."""

        to_use = to_partition
        # Pad (if requested) to include last characters as starting characters in n-grams.        
        if self.pad_string:
            to_use += "\0" * (self.ngram_size - 1)

        # Break into overlapping n-grams
        for iFrom in range(len(to_use) - self.ngram_size + 1):
            yield to_partition[iFrom : (iFrom + self.ngram_size)]


class AsymmetricNGramGraph(ProximityGraph):
    def __init__(self, n=3, Dwin=3, data : str = None):
        super().__init__()

        self.n = n
        self.Dwin = Dwin
        self.data = data

        if data is not None:
            self._calculate_graph()


    def _calculate_graph(self):
        partitionable_data = PartitionableString(self.data)
        partitions = list(TextNGramPartitioner(self.n).partition(partitionable_data))

        # For each sequence in the partition (but the last)
        for iReferenceIndex in range(len(partitions)):
            # Set starting and ending neighbour
            iFirstNeighbour, iLastNeighbour = (iReferenceIndex + 1, 
                min(iReferenceIndex + self.Dwin, len(partitions) - 1))
            # For each neighbour from iFirstN... to iLastN... + 1 noninclusively
            for iProximityCnt in range(iFirstNeighbour, iLastNeighbour + 1):

                # Get the partitions
                u_of_edge,v_of_edge = (partitions[iReferenceIndex], partitions[iProximityCnt])
                # If the edge does not exist
                if not self.has_edge(u=u_of_edge,v=v_of_edge):
                    # Initialize it
                    self.add_edge(u_of_edge=u_of_edge, v_of_edge=v_of_edge, weight = 1.0)
                else:
                    # else update the weight
                    self.update_edge_weight(u=u_of_edge, v=v_of_edge)

    def update_edge_weight(self, u, v):
        new_weight = self.get_edge_data(u=u, v=v)['weight'] + 1.0
        self.edges[u, v]['weight'] = new_weight
        



class SymmetricNGramGraph(ProximityGraph):
    def __init__(self, n=3, Dwin=3, data : str = None):
        super().__init__()

        self.n = n
        self.Dwin = Dwin
        self.data = data

        if data is not None:
            self._calculate_graph()


    def _calculate_graph(self):
        partitionable_data = PartitionableString(self.data)
        partitions = list(TextNGramPartitioner(self.n).partition(to_partition=partitionable_data))

        # For each sequence in the partition
        for iReferenceIndex in range(len(partitions)):
            iFirstNeighbour, iLastNeighbour = (max(iReferenceIndex - self.Dwin, 0), 
                min(iReferenceIndex + self.Dwin + 1, len(partitions)))

            for iNeighbourIndex in range(iFirstNeighbour, iLastNeighbour):
                if iReferenceIndex == iNeighbourIndex: # Ignore self
                    continue

                u_of_edge,v_of_edge = (partitions[iReferenceIndex], partitions[iNeighbourIndex])

                # Apply an ordering to the edges
                if u_of_edge > v_of_edge:
                    tmp_edge = v_of_edge
                    v_of_edge = u_of_edge
                    u_of_edge = tmp_edge

                # If the edge is new
                if not self.has_edge(u=u_of_edge,v=v_of_edge) :
                    # Add it
                    self.add_edge(u_of_edge=u_of_edge, v_of_edge=v_of_edge, weight = 1.0)
                else:
                    # Else update its weight
                    self.update_edge_weight(u=u_of_edge, v=v_of_edge)

    def update_edge_weight(self, u, v):
        new_weight = self.get_edge_data(u=u, v=v)['weight'] + 1.0
        self.edges[u, v]['weight'] = new_weight
