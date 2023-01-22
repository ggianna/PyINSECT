from pyinsect.graphs.proximity_graphs import *
from typing import Tuple
import json

class Similarity:
    def __init__(self, value : float = None, new_components: dict = None) -> None:
        self.components = new_components
        self.value = value

    @property
    def components(self):
        return self.components
    
    @components.setter
    def set_components(self, new_components: dict):
        self.components = new_components

    @property
    def value(self):
        """This function can be overriden to calculate the final value based on the components"""
        return self.value

    def __str__(self) -> str:
        return f"{self.value} " + json.dumps(self.components)

class BaseSimilarityOperator(ABC):
    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns a tuple containing a Similarity object. The similarity respects the directionality of the call: 
        it measures how similar is the info_evaluated to the reference_info."""
        
        raise NotImplementedError()
    
class BaseMergeOperator(ABC):
    def merge(base_info: ProximityInformation, new_info: ProximityInformation, update_inline: bool, *args, **kwargs) -> ProximityInformation:
        """Returns a proximity graph, which is the merging of the two ProximityInformation objects, respecting the directionality (we begin from 
        base_info and merge new_info to it. If update_inline is True, then the base_graph should be updated inline, otherwise
        a new ProximityInformation object should be created and returned.
        
        The remaining positional and keyword arguments can support operators, such as the weighted update operator."""
        
        raise NotImplementedError()

class BaseMinusOperator(ABC):
    def minus(base_info: ProximityInformation, other_info: ProximityInformation) -> ProximityInformation:
        """Returns a proximity graph, which is the difference of the two ProximityInformation objects, respecting the directionality (we 
        reduce (whatever this means based on the implementation) the information of base_info by what other_info contains."""    

        raise NotImplementedError()

class SizeSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SS" : 0.0}
        super().__init__()

    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        reference_info_graph = reference_info.as_graph().edges
        info_evaluated_graph = info_evaluated.as_graph().edges

        nominator = min(len(reference_info_graph), len(info_evaluated_graph))
        denominator = max(len(reference_info_graph), len(info_evaluated_graph))

        return Similarity(nominator / denominator, new_components={"SS": nominator / denominator})

class AsymmetricContainmentSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"ACS" : 0.0}
        super().__init__()

    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns which percentage of the proximities existing in reference_info is contained in info_evaluated."""

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges

        nominator = len(nx.intersection(reference_info, info_evaluated))
        denominator = len(reference_info_set)

        return Similarity(nominator / denominator, new_components={"ACS": nominator / denominator})

class SymmetricContainmentSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SCS" : 0.0}
        super().__init__()

    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the ratio of common info between info_evaluated and reference_info, with respect to the size of 
        the biggest of the two."""

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        if len(reference_info_set) < len(info_evaluated_set):
            bigger_set = info_evaluated_set
            smaller_set = reference_info_set
        else:
            bigger_set = reference_info_set
            smaller_set = info_evaluated_set

        nominator = len(nx.intersection(smaller_set, bigger_set))
        denominator = len(bigger_set)

        return Similarity(nominator / denominator, new_components={"SCS": nominator / denominator})

class AsymmetricValueSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"AVS" : 0.0}
        super().__init__()

    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the value similarity, which is the result of dividing the following:

            Nominator: the sum of the ratios of the values of common proximity items between the two given info sets, where in the ratio
            the biggest value goes to the denominator of the ratio and the smallest of the two to the nominator.
            
            Denominator: the size of the reference_info.
        """

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        common_edge_set = nx.intersection(reference_info_set, info_evaluated_set)
        overall_contriubtions = 0.0
        for cur_edge in common_edge_set:
            min_val = min(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight'])
            max_val = max(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight'])
            contribution = min_val / max_val
            overall_contriubtions += contribution
        res = contribution / len(reference_info_set)

        return Similarity(res, new_components={"AVS": res})

class SymmetricValueSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SVS" : 0.0}
        super().__init__()

    def similarity(reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the value similarity, which is the result of dividing the following:

            Nominator: the sum of the ratios of the values of common proximity items between the two given info sets, where in the ratio
            the biggest value goes to the denominator of the ratio and the smallest of the two to the nominator.
            
            Denominator: the size of the bigger of the two compared information sets.
        """

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        common_edge_set = nx.intersection(reference_info_set, info_evaluated_set)
        overall_contriubtions = 0.0
        for cur_edge in common_edge_set:
            min_val = min(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight'])
            max_val = max(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight'])
            contribution = min_val / max_val
            overall_contriubtions += contribution
        res = contribution / max(len(reference_info_set), len(info_evaluated_set))

        return Similarity(res, new_components={"SVS": res})

