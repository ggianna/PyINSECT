import concurrent
import unittest

from pyinsect.collector.NGramGraphCollector import (
    ArrayGraph2DCollector,
    HPG2DCollector,
    HPG2DCollectorParallel,
)
from tests.base import BaseParallelTestCase, BaseTestCase
from tests.hpg_collector.base import Collector2DTestCaseMixin


class ArrayGraph2DCollectorTestCase(Collector2DTestCaseMixin, BaseTestCase):
    collector_type = ArrayGraph2DCollector
    scores = [0.72, 0.876, 0.042]


class HPG2DCollectorTestCase(Collector2DTestCaseMixin, BaseTestCase):
    collector_type = HPG2DCollector


class HPG2DCollectorParallelTestCase(Collector2DTestCaseMixin, BaseParallelTestCase):
    collector_type = HPG2DCollectorParallel

    def _construct_collector(self, *args, **kwargs):
        return super()._construct_collector(pool=self.pool)

    def test_concurrency_on_graph_construction(self):
        collector = self._construct_collector()

        for entry in self.train_data:
            collector.add(entry)

    @unittest.skip("due to deadlock")
    def test_concurrency_on_all_levels(self):
        futures = []

        collector = self._construct_collector()

        for surface in self.train_data:
            future = self.pool.submit(collector._construct_graph, surface)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            collector._add_graph(future.result())
