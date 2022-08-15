import os
from config import load_conf as load, load_collector_opts

if __name__ == "__main__":
    """ Generate data from here. """

    c = load(load_collector_opts)

    print(c)