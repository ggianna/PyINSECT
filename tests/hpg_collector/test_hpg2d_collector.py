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
