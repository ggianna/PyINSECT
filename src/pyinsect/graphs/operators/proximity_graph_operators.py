from pyinsect.graphs.proximity_graphs import *
from typing import Tuple
import json

class Similarity:
    def __init__(self, value : float = None, new_components: dict = None) -> None:
        # Initialize and assign values using mutators, where available
        self._components = new_components
        self._value = value

    @property
    def components(self):
        return self._components
    
    @components.setter
    def set_components(self, new_components: dict):
        self._components = new_components

    @property
    def value(self):
        """This function can be overriden to calculate the final value based on the components"""
        return self._value

    def __str__(self) -> str:
        return f"{self.value} " + json.dumps(self.components)

class BaseSimilarityOperator(ABC):
    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns a tuple containing a Similarity object. The similarity respects the directionality of the call: 
        it measures how similar is the info_evaluated to the reference_info."""
        
        raise NotImplementedError()
    
class BaseMergeOperator(ABC):
    def merge(self, base_info: ProximityInformation, new_info: ProximityInformation, update_inline: bool, *args, **kwargs) -> ProximityInformation:
        """Returns a proximity graph, which is the merging of the two ProximityInformation objects, respecting the directionality (we begin from 
        base_info and merge new_info to it. If update_inline is True, then the base_graph should be updated inline, otherwise
        a new ProximityInformation object should be created and returned.
        
        The remaining positional and keyword arguments can support operators, such as the weighted update operator."""
        
        raise NotImplementedError()

class BaseMinusOperator(ABC):
    def minus(self, base_info: ProximityInformation, other_info: ProximityInformation) -> ProximityInformation:
        """Returns a proximity graph, which is the difference of the two ProximityInformation objects, respecting the directionality (we 
        reduce (whatever this means based on the implementation) the information of base_info by what other_info contains."""    

        raise NotImplementedError()

