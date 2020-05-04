#!/usr/bin/env python

import logging
import os
import string
import sys

from wazo_auth_client import Client as AuthClient
from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy, parse_config_file
from wazo_provd_client import Client as ProvdClient

logger = logging.getLogger('update_voip_ip_address')

logging.basicConfig(level=logging.INFO)

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-upgrade/config.yml',
    'auth': {
        'key_file': '/var/lib/wazo-auth-keys/wazo-upgrade-key.yml'
    }
}

ip = sys.argv[1]

def load_config():
    file_config = read_config_file_hierarchy(_DEFAULT_CONFIG)
    key_config = _load_key_file(ChainMap(file_config, _DEFAULT_CONFIG))
    return ChainMap(key_config, file_config, _DEFAULT_CONFIG)


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {'auth': {'username': key_file['service_id'],
                     'password': key_file['service_key']}}

config = load_config()

auth_client = AuthClient(**config['auth'])
token_data = auth_client.token.new(expiration=300)

logger.info("Connecting to provd...")
provd_client = ProvdClient(token=token_data['token'], **config['provd'])
config_manager = provd_client.configs

logger.info("Fetching default device template...")
default_config = config_manager.get('defaultconfigdevice')

logger.info("Updating phonebook ip and ntp ip")
raw_config = default_config['raw_config']

raw_config['ntp_ip'] = ip
raw_config['X_xivo_phonebook_ip'] = ip
logger.info("Updating config...")
config_manager.update(default_config)
 
logger.info("Fetching default provd config...")
default_config = config_manager.get('default')

logger.info("Updating provd ip")
raw_config = default_config['raw_config']

raw_config['ip'] = ip
logger.info("Updating config...")
config_manager.update(default_config)

logger.info("Fetching default base config...")
default_config = config_manager.get('base')

logger.info("Updating phonebook ip")
raw_config = default_config['raw_config']

raw_config['ntp_ip'] = ip
raw_config['X_xivo_phonebook_ip'] = ip
logger.info("Updating config...")
config_manager.update(default_config)

logger.info("Fetching autoprov config...")
default_config = config_manager.get('autoprov')

logger.info("Updating autoprov config")
raw_config = default_config['raw_config']

raw_config['sccp_call_managers']['1']['ip'] = ip
raw_config['sip_lines']['1']['proxy_ip'] = ip

logger.info("Updating config...")
config_manager.update(default_config)

logger.info("Fetching registrar config...")
default_config = config_manager.list_registrar()

logger.info("Updating all proxy and registrar ip")
for config in default_config['configs']:
  config['registrar_main'] = ip
  config['proxy_main'] = ip
  config_manager.update(config)

logger.info('Done.')

