from pyinsect.graphs.operators.proximity_graph_operators import BaseSimilarityOperator, Similarity
from pyinsect.graphs.proximity_graphs import ProximityInformation
import networkx as nx

class SizeSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SS" : 0.0}
        super().__init__()

    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        reference_info_graph = reference_info.as_graph().edges
        info_evaluated_graph = info_evaluated.as_graph().edges

        nominator = float(min(len(reference_info_graph), len(info_evaluated_graph)))
        denominator = float(max(len(reference_info_graph), len(info_evaluated_graph)))

        return Similarity(nominator / denominator, new_components={"SS": nominator / denominator})

class AsymmetricContainmentSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"ACS" : 0.0}
        super().__init__()

    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns which percentage of the proximities existing in reference_info is contained in info_evaluated."""

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges

        nominator = float(len(nx.intersection(reference_info, info_evaluated)))
        denominator = float(len(reference_info_set))

        return Similarity(nominator / denominator, new_components={"ACS": nominator / denominator})

class SymmetricContainmentSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SCS" : 0.0}
        super().__init__()

    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the ratio of common info between info_evaluated and reference_info, with respect to the size of 
        the biggest of the two."""

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        if len(reference_info_set) < len(info_evaluated_set):
            bigger_set = info_evaluated_set
        else:
            bigger_set = reference_info_set

        nominator = float(len(nx.intersection(reference_info.as_graph(), info_evaluated.as_graph()).edges))
        denominator = float(len(bigger_set))

        return Similarity(nominator / denominator, new_components={"SCS": nominator / denominator})

class AsymmetricValueSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"AVS" : 0.0}
        super().__init__()

    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the value similarity, which is the result of dividing the following:

            Nominator: the sum of the ratios of the values of common proximity items between the two given info sets, where in the ratio
            the biggest value goes to the denominator of the ratio and the smallest of the two to the nominator.
            
            Denominator: the size of the reference_info.
        """

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        common_edge_set = nx.intersection(reference_info.as_graph(), info_evaluated.as_graph()).edges
        overall_contriubtions = 0.0
        for cur_edge in common_edge_set:
            min_val = float(min(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight']))
            max_val = float(max(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight']))
            contribution = min_val / max_val
            overall_contriubtions += contribution
        res = overall_contriubtions / float(len(reference_info_set))

        return Similarity(res, new_components={"AVS": res})

class SymmetricValueSimilarity(BaseSimilarityOperator):

    def __init__(self) -> None:
        self.components = {"SVS" : 0.0}
        super().__init__()

    def similarity(self, reference_info: ProximityInformation, info_evaluated: ProximityInformation) -> Similarity:
        """Returns the value similarity, which is the result of dividing the following:

            Nominator: the sum of the ratios of the values of common proximity items between the two given info sets, where in the ratio
            the biggest value goes to the denominator of the ratio and the smallest of the two to the nominator.
            
            Denominator: the size of the bigger of the two compared information sets.
        """

        reference_info_set = reference_info.as_graph().edges
        info_evaluated_set = info_evaluated.as_graph().edges
        common_edge_set = nx.intersection(reference_info.as_graph(), info_evaluated.as_graph()).edges
        overall_contributions = 0.0
        for cur_edge in common_edge_set:
            min_val = float(min(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight']))
            max_val = float(max(reference_info_set[cur_edge]['weight'], info_evaluated_set[cur_edge]['weight']))
            contribution = min_val / max_val
            overall_contributions += contribution
        res = overall_contributions / float(max(len(reference_info_set), len(info_evaluated_set)))

        return Similarity(res, new_components={"SVS": res})

