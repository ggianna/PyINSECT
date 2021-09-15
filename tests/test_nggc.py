from pyinsect.collector.NGramGraphCollector import NGramGraphCollector
from tests.base import BaseTestCase


class NGramGraphCollectorTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.train_data = [
            "A test...",
            "Another, bigger test. But a test, anyway...",
        ]

        self.test_data = [
            ("A test...", 0.5959),
            ("Another, bigger test...", 0.8530),
            ("Something irrelevant!", 0),
        ]

        self.collector = NGramGraphCollector()

        for entry in self.train_data:
            self.collector.add(entry)

    def test_appropriateness_of(self):
        for entry, expected in self.test_data:
            with self.subTest(query=entry):
                self.assertAlmostEqual(
                    self.collector.appropriateness_of(entry), expected, places=3
                )
