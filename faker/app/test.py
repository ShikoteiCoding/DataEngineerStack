import unittest
import os

from config import load_conf as load, load_collector_opts

VALID_COLLECTOR_ENDPOINT = "valid_collector_url"

class TestConfig(unittest.TestCase):
    """ Test Config Loadings """

    def setUp(self):
        os.environ["COLLECTOR_ENDPOINT"] = VALID_COLLECTOR_ENDPOINT

    def test_load_collector(self):
        c = load(load_collector_opts)

        self.assertEqual(c.collector_url, VALID_COLLECTOR_ENDPOINT)

if __name__ == '__main__':
    unittest.main()