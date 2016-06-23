# -*- coding: utf-8 -*-

import click

from blackgate.core import component
from blackgate.config import parse_yaml_config
from blackgate.config import read_yaml_config
from blackgate.config import read_default_config
from blackgate.server import run


@click.group()
@click.option('-c', '--config', default='')
@click.pass_context
def main(ctx, config):
    if not config:
        config = read_default_config()
    else:
        config = read_yaml_config(config)

    if not config:
        ctx.fail('config not found.')

    try:
        config = parse_yaml_config(config)
    except ValueError:
        ctx.fail('config is not valid yaml.')

    ctx.obj['config'] = config


@main.command()
@click.pass_context
def start(ctx):
    config = ctx.obj['config']
    component.configurations = config
    component.install()
    run(config.get('port', 9654))


if __name__ == '__main__':
    main()
