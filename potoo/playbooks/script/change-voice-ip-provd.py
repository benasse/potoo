#!/usr/bin/env python

import logging
import os
import string
import sys

from wazo_auth_client import Client as AuthClient
from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy, parse_config_file
from wazo_provd_client import Client as ProvdClient
from wazo_confd_client import Client as ConfdClient

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
logger.info('Done.')

logger.info("Connecting to confd..")

confd_client = ConfdClient(token=token_data['token'], **config['confd'])
registrars = confd_client.registrars.list()
registrars['items'][0]['main_host'] = ip
registrars['items'][0]['proxy_main_host'] = ip
 
logger.info("Update registrar and reconfigure devices...")
confd_client.registrars.update(registrars['items'][0])
logger.info("Done.")
