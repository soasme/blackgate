# -*- coding: utf-8 -*-

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
