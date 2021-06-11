import concurrent

from pyinsect.collector.NGramGraphCollector import (
    HPG2DCollector,
    HPG2DCollectorParallel,
)
from tests.base import BaseTestCase
from tests.hpg_collector.base import HPGCollectorTestCaseMixin


class HPG2DCollectorTestCase(HPGCollectorTestCaseMixin, BaseTestCase):
    collector_type = HPG2DCollector


class HPG2DCollectorParallelTestCase(HPGCollectorTestCaseMixin, BaseTestCase):
    collector_type = HPG2DCollectorParallel

    def test_concurrency_on_graph_construction(self):
        with concurrent.futures.ProcessPoolExecutor(2) as pool:
            collector = self.collector_type(pool=pool)

            for entry in self.train_data:
                collector.add(entry)

    def test_concurrency_on_all_levels(self):
        results = []
        with concurrent.futures.ProcessPoolExecutor(2) as pool:
            futures = []

            collector = self.collector_type(pool=pool)

            for surface in self.train_data:
                future = pool.submit(collector._construct_graph, surface)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        for result in results:
            collector._add_graph(result)
