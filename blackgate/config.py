# -*- coding: utf-8 -*-

import os
import yaml
from blackgate.errors import InvalidConfig

def verify_proxy(conf):
    if not conf.get('proxies'):
        return
    for proxy in conf.get('proxies'):
        if 'upstream_url' not in proxy:
            raise InvalidConfig('Missing Upstream URL, example: `upstream_url: http://service.com`')
        if 'name' not in proxy:
            raise InvalidConfig('Missing Upstream Name, example: `name: myservice')



def parse_yaml_config(config):
    try:
        return yaml.load(config)
    except ValueError:
        raise InvalidConfig('Broken YAML config.')


def read_yaml_config(path):
    try:
        with open(path) as f:
            return f.read()
    except IOError:
        pass

def read_default_config():
    config = (
        read_yaml_config(os.path.join(os.getcwd(), 'blackgate.yml')) or \
        read_yaml_config(os.path.join(os.getlogin(), '.blackgate.yml')) or \
        read_yaml_config(os.path.join('usr', 'local', 'etc', 'blackgate', 'blackgate.yml')) or \
        read_yaml_config(os.path.join('etc', 'blackgate', 'blackgate.yml'))
    )
    return config
