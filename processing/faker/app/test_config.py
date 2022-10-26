import unittest
import os

from config import load_conf as load, load_collector_opts

COLLECTOR_URL = "hostname:8080"
HTTP_COLLECTOR_URL = "http://hostname:8080"

class TestConfig(unittest.TestCase):
    """ Test Config Loadings """

    def setUp(self):
        os.environ["COLLECTOR_URL"] = COLLECTOR_URL

    def test_load_collector(self):
        c = load(load_collector_opts)

        self.assertEqual(c.collector_url, COLLECTOR_URL)

    def test_url_collector(self):
        c = load(load_collector_opts)

        self.assertEqual(c._http_collector_url, HTTP_COLLECTOR_URL)

        
if __name__ == '__main__':
    unittest.main()