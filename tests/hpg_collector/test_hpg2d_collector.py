import unittest

from pyinsect.collector.NGramGraphCollector import (
    HPG2DCollector,
    HPG2DCollectorParallel,
)
from tests.hpg_collector.base import HPGCollectorTestCaseMixin


class HPG2DCollectorTestCase(HPGCollectorTestCaseMixin, unittest.TestCase):
    collector_type = HPG2DCollector


class HPG2DCollectorParallelTestCase(HPGCollectorTestCaseMixin, unittest.TestCase):
    collector_type = HPG2DCollectorParallel
