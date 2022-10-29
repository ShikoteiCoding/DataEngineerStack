import unittest
import os

from config import load as load_config

OUTPUT = "collector"
COLLECTOR_URL = "collector:8080"

sample_configuration = """
output:
    collector:
        endpoint: collector:8080
"""

class TestYaml(unittest.TestCase):
    """ Test Config Loadings """

    def test_settings(self):
        c = load_config(sample_configuration)
        self.assertEqual(c["output"]["collector"]["endpoint"], COLLECTOR_URL)

        
if __name__ == '__main__':
    unittest.main()