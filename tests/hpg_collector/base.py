import random
import string


class HPGCollectorTestCaseMixin(object):
    collector_type = None

    def setUp(self):
        super().setUp()

        random.seed(1234)

        self.train_data = [
            self.generate_random_2d_int_array(4),
            self.generate_random_2d_int_array(5),
        ]

        self.test_data = [
            (self.train_data[0], 0.5),
            (self.transpose(self.train_data[1]), 0.5),
            (self.generate_random_2d_int_array(6), 0.001),
        ]

        self.collector = self.collector_type()

        for entry in self.train_data:
            self.collector.add(entry)

    def test_appropriateness_of(self):
        for index, (entry, expected) in enumerate(self.test_data):
            with self.subTest(
                collector=self.collector_type, index=index, expected=expected
            ):
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
