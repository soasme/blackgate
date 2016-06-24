# -*- coding: utf-8 -*-

import click

from blackgate.core import component
from blackgate.config import parse_yaml_config
from blackgate.config import read_yaml_config
from blackgate.config import read_default_config
from blackgate.server import Server


@click.group()
@click.option('-c', '--config', default='')
@click.option('--daemon/--no-daemon', default=True)
@click.option('--pidfile')
@click.pass_context
def main(ctx, config, daemon, pidfile):
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

    component.configurations = config
    component.install()

    if not pidfile:
        pidfile = config['pidfile']
    if not pidfile:
        pidfile = '/var/run/blackgate.pid'

    ctx.obj = {}
    ctx.obj['server'] = Server(pidfile)
    ctx.obj['daemon'] = daemon



@main.command()
@click.pass_context
def start(ctx):
    if ctx.obj['daemon']:
        ctx.obj['server'].start()
    else:
        ctx.obj['server'].run()

@main.command()
@click.pass_context
def stop(ctx):
    server = ctx.obj['server']
    server.stop()


@main.command()
@click.pass_context
def restart(ctx):
    server = ctx.obj['server']
    server.restart()

@main.command()
@click.pass_context
def status(ctx):
    server = ctx.obj['server']
    server.is_running()



if __name__ == '__main__':
    main()
