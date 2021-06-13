import concurrent

from pyinsect.collector.NGramGraphCollector import (
    HPG2DCollector,
    HPG2DCollectorParallel,
)
from tests.base import BaseParallelTestCase, BaseTestCase
from tests.hpg_collector.base import HPGCollectorTestCaseMixin


class HPG2DCollectorTestCase(HPGCollectorTestCaseMixin, BaseTestCase):
    collector_type = HPG2DCollector


class HPG2DCollectorParallelTestCase(HPGCollectorTestCaseMixin, BaseParallelTestCase):
    collector_type = HPG2DCollectorParallel

    def _construct_collector(self, *args, **kwargs):
        return super()._construct_collector(pool=self.pool)

    def test_concurrency_on_graph_construction(self):
        collector = self._construct_collector()

        for entry in self.train_data:
            collector.add(entry)

    def test_concurrency_on_all_levels(self):
        futures = []

        collector = self._construct_collector()

        for surface in self.train_data:
            future = self.pool.submit(collector._construct_graph, surface)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            collector._add_graph(future.result())
