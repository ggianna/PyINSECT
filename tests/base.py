import logging
import time
import unittest

logger = logging.getLogger(__name__)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._start_time = time.time()

    def tearDown(self):
        logger.debug("%s took %07.3f" % (self.id(), time.time() - self._start_time))

    def run(self, result=None):
        if not result.errors:
            super().run(result)
