import unittest

from pyinsect.collector.NGramGraphCollector import NGramGraphCollector


class NGramGraphCollectorTestCase(unittest.TestCase):
    train_data = [
        "A test...",
        "Another, bigger test. But a test, anyway...",
    ]

    test_data = [
        ("A test...", 0.5959),
        ("Another, bigger test...", 0.8530),
        ("Something irrelevant!", 0),
    ]

    def setUp(self):
        self.collector = NGramGraphCollector()

        for entry in self.train_data:
            self.collector.addText(entry)

    def test_getAppropriateness(self):
        for entry, expected in self.test_data:
            with self.subTest(query=entry):
                self.assertAlmostEqual(
                    self.collector.getAppropriateness(entry), expected, places=3
                )
