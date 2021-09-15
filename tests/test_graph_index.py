from pyinsect.documentModel.comparators.NGramGraphSimilarity import SimilarityNVS
from pyinsect.documentModel.representations.DocumentNGramGraph import DocumentNGramGraph
from pyinsect.indexing.graph_index import GraphIndex
from tests.base import BaseTestCase


class GraphIndexTestCase(BaseTestCase):
    train_data = [
        "Life isn’t about getting and having, it’s about giving and being.",
        "Whatever the mind of man can conceive and believe, it can achieve.",
        "Strive not to be a success, but rather to be of value.",
        "Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference.",
        "I attribute my success to this: I never gave or took any excuse.",
        "You miss 100% of the shots you don’t take.",
        "I’ve missed more than 9000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life. And that is why I succeed.",
        "The most difficult thing is the decision to act, the rest is merely tenacity.",
    ]

    def setUp(self):
        super().setUp()

        self.graph_index = GraphIndex(SimilarityNVS())

    def test_when_empty_all_different_should_return_different_indices(self):
        for index, entry in enumerate(self.train_data):
            graph = DocumentNGramGraph(Data=entry)

            with self.subTest(
                index=index,
                entry="{0}...".format(
                    entry[:20],
                ),
            ):
                self.assertEqual(self.graph_index[graph], index)

    def test_when_empty_all_same_should_return_same_index(self):
        for entry in [
            self.train_data[0],
        ] * len(self.train_data):
            graph = DocumentNGramGraph(Data=entry)

            with self.subTest(
                entry="{0}...".format(
                    entry[:20],
                )
            ):
                self.assertEqual(self.graph_index[graph], 0)

    def test_when_not_empty_all_different_should_return_matching_indices(self):
        for index, entry in enumerate(self.train_data[:3]):
            self.graph_index[DocumentNGramGraph(Data=entry)]

        for index, entry in enumerate(self.train_data[:3]):
            graph = DocumentNGramGraph(Data=entry)

            with self.subTest(
                index=index,
                entry="{0}...".format(
                    entry[:20],
                ),
            ):
                self.assertEqual(self.graph_index[graph], index)
