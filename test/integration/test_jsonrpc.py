import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from dinerod import DineroDaemon
from dinero_config import DineroConfig


def test_dinerod():
    config_text = DineroConfig.slurp_config_file(config.dinero_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009110a70cd2bf2cdcae9a8b1425bb074c7b7b08570c2c9f04fe8668c6589'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000008a8a0d4d1490b99bc94122b023c72e8adf4adac2f00bc4d5344eb4548d7'

    creds = DineroConfig.get_rpc_creds(config_text, network)
    dinerod = DineroDaemon(**creds)
    assert dinerod.rpc_command is not None

    assert hasattr(dinerod, 'rpc_connection')

    # Dinero testnet block 0 hash == 000009110a70cd2bf2cdcae9a8b1425bb074c7b7b08570c2c9f04fe8668c6589
    # test commands without arguments
    info = dinerod.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert dinerod.rpc_command('getblockhash', 0) == genesis_hash
