import random
import string


class Collector2DTestCaseMixin(object):
    collector_type = None
    scores = [0.5, 0.5, 0.001]

    def _construct_collector(self, *args, **kwargs):
        return self.collector_type(*args, **kwargs)

    def setUp(self):
        super().setUp()

        random.seed(1234)

        self.train_data = [
            self.generate_random_2d_int_array(4),
            self.generate_random_2d_int_array(5),
        ]

        self.test_data = list(
            zip(
                [
                    self.train_data[0],
                    self.transpose(self.train_data[1]),
                    self.generate_random_2d_int_array(6),
                ],
                self.scores,
            )
        )

    def test_appropriateness_of(self):
        collector = self._construct_collector()

        for entry in self.train_data:
            collector.add(entry)

        for index, (entry, expected) in enumerate(self.test_data):
            with self.subTest(
                collector=self.collector_type, index=index, expected=expected
            ):
                self.assertAlmostEqual(
                    collector.appropriateness_of(entry), expected, places=3
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
