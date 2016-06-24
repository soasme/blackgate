# -*- coding: utf-8 -*-

import click

from blackgate.core import component
from blackgate.config import parse_yaml_config
from blackgate.config import read_yaml_config
from blackgate.config import read_default_config
from blackgate.server import Server


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

    ctx.obj = {}
    ctx.obj['config'] = config


@main.command()
@click.option('--daemon/--no-daemon', default=True)
@click.option('--pidfile', default='/var/run/blackgate.pid')
@click.pass_context
def start(ctx, daemon, pidfile):
    config = ctx.obj['config']
    component.configurations = config
    component.install()

    if pidfile != config['pidfile']:
        pidfile = config['pidfile']

    daemon = Server(pidfile)

    if daemon:
        daemon.start()
    else:
        daemon.run()

@main.command()
@click.option('--pidfile', default='/var/run/blackgate.pid')
@click.pass_context
def stop(ctx, pidfile):
    config = ctx.obj['config']
    component.configurations = config
    component.install()

    if pidfile != config['pidfile']:
        pidfile = config['pidfile']

    daemon = Server(pidfile)
    daemon.stop()


@main.command()
@click.option('--pidfile', default='/var/run/blackgate.pid')
@click.pass_context
def restart(ctx, pidfile):
    config = ctx.obj['config']
    component.configurations = config
    component.install()

    if pidfile != config['pidfile']:
        pidfile = config['pidfile']

    daemon = Server(pidfile)
    daemon.restart()



if __name__ == '__main__':
    main()
