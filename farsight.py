#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import gc
import sys
import json
import iffsdkpy

from pathlib import Path
from iffsdkpy import Chain


def load_config(filename):
    with open(filename, 'r') as cfg_file:
        config = json.load(cfg_file)

    if 'IFF' not in config:
        print("Invalid configuration provided: missing `IFF` section", file=sys.stderr)
        sys.exit(1)

    if 'chains' not in config:
        print("Invalid configuration provided: missing `chains` section", file=sys.stderr)
        sys.exit(1)

    if len(config['chains']) == 0:
        print("Invalid configuration provided: section `chains` must not be empty", file=sys.stderr)
        sys.exit(1)

    if not isinstance(config['chains'], list):
        print("Invalid configuration provided: section `chains` must be an array", file=sys.stderr)
        sys.exit(1)

    return config

def create_chains(chains_config):

    def error_handler(element_id, error_code):
        pass

    chains = list(map(
        lambda chain: Chain(
            json.dumps(chain),
            error_handler
        ),
        chains_config
    ))

    iffsdkpy.log(iffsdkpy.log_level.info, Path(__file__).stem, "Press Enter to terminate the program")
    input("")

    del chains
    gc.collect()

def main():
    config = load_config(Path(__file__).stem + '.json')

    iff_config = json.dumps(config['IFF'])
    iffsdkpy.initialize(iff_config)

    create_chains(config['chains'])

    iffsdkpy.finalize()

if __name__ == '__main__':
    main()
