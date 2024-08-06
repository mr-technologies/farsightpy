#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# std
import gc
import json
from pathlib import Path
import sys

# IFF SDK
import iffsdkpy
from iffsdkpy import Chain


def load_config(filename):
    with open(filename, 'r') as cfg_file:
        config = json.load(cfg_file)

    if 'IFF' not in config:
        sys.exit("Invalid configuration provided: missing `IFF` section")

    if 'chains' not in config:
        sys.exit("Invalid configuration provided: missing `chains` section")

    if len(config['chains']) == 0:
        sys.exit("Invalid configuration provided: section `chains` must not be empty")

    if not isinstance(config['chains'], list):
        sys.exit("Invalid configuration provided: section `chains` must be an array")

    return config

def create_chains(chains_config):

    def error_handler(element_id, error_code):
       iffsdkpy.log(iffsdkpy.log_level.error, Path(__file__).stem, f"Chain element `{element_id}` reported an error: {error_code}")

    return list(map(
        lambda chain: Chain(
            json.dumps(chain),
            error_handler
        ),
        chains_config
    ))

def main():
    config = load_config(Path(__file__).stem + '.json')

    iff_config = json.dumps(config['IFF'])
    iffsdkpy.initialize(iff_config)

    chains = create_chains(config['chains'])

    iffsdkpy.log(iffsdkpy.log_level.info, Path(__file__).stem, "Press Enter to terminate the program")
    input()

    del chains
    gc.collect()

    iffsdkpy.finalize()

if __name__ == '__main__':
    main()
