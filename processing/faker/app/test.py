import unittest
import os

from config import load_conf as load, load_collector_opts

VALID_COLLECTOR_HOST = "hostname"
VALID_COLLECTOR_PORT = "8080"
VALID_COLLECTOR_URL = "http://hostname:8080"

class TestConfig(unittest.TestCase):
    """ Test Config Loadings """

    def setUp(self):
        os.environ["COLLECTOR_HOST"] = VALID_COLLECTOR_HOST
        os.environ["COLLECTOR_PORT"] = VALID_COLLECTOR_PORT

    def test_load_collector(self):
        c = load(load_collector_opts)

        self.assertEqual(c.collector_host, VALID_COLLECTOR_HOST)
        self.assertEqual(c.collector_port, VALID_COLLECTOR_PORT)

    def test_url_collector(self):
        c = load(load_collector_opts)

        self.assertEqual(c._collector_url, VALID_COLLECTOR_URL)

        c.collector_host = None
        self.assertEqual(c._collector_url, "")
        c.collector_port = None
        self.assertEqual(c._collector_url, "")

        

if __name__ == '__main__':
    unittest.main()