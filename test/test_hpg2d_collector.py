import random
import string
import unittest

from pyinsect.collector.NGramGraphCollector import HPG2DCollector


class HPG2DCollectorTestCase(unittest.TestCase):
    def setUp(self):
        random.seed(1234)

        self.train_data = [
            self.generate_random_2d_int_array(4),
            self.generate_random_2d_int_array(5),
        ]

        self.test_data = [
            (self.train_data[0], 0.5),
            (self.transpose(self.train_data[1]), 0.5),
            (self.generate_random_2d_int_array(6), 0),
        ]

        self.collector = HPG2DCollector()

        for entry in self.train_data:
            self.collector.add(entry)

    def test_appropriateness_of(self):
        for entry, expected in self.test_data:
            with self.subTest(query=entry):
                self.assertAlmostEqual(
                    self.collector.appropriateness_of(entry), expected, places=3
                )

    @classmethod
    def generate_random_2d_int_array(cls, size):
        return [
            [ord(random.choice(string.ascii_letters)) for _ in range(size)]
            for _ in range(size)
        ]

    @classmethod
    def transpose(cls, matrix_2d):
        return list(map(list, zip(*matrix_2d)))
