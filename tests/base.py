import concurrent
import logging
import os
import time
import unittest

logger = logging.getLogger(__name__)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._start_time = time.time()

    def tearDown(self):
        logger.debug("%s took %07.3f" % (self.id(), time.time() - self._start_time))


class BaseParallelTestCase(unittest.TestCase):
    def setUp(self):
        self._pool = concurrent.futures.ProcessPoolExecutor(os.cpu_count())

    def tearDown(self):
        self._pool.shutdown(wait=True)

    @property
    def pool(self):
        return self._pool
