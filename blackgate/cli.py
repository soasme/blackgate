# -*- coding: utf-8 -*-

import os
import click

from tornado.web import Application
from blackgate.component import Component
from blackgate.config import parse_yaml_config
from blackgate.config import read_yaml_config
from blackgate.config import read_default_config
from blackgate.server import Server


@click.group()
@click.option('-c', '--config', default='')
@click.option('--daemon/--no-daemon', default=True)
@click.option('--pidfile', default='/var/run/blackgate.pid')
@click.option('--stdin', default=os.devnull)
@click.option('--stdout', default=os.devnull)
@click.option('--stderr', default=os.devnull)
@click.option('--directory', default='.')
@click.option('--umask', type=int, default=022)
@click.pass_context
def main(ctx, config, daemon, pidfile,
         stdin, stdout, stderr, directory, umask):
    """Entry of Blackgate command."""
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

    component = Component()
    component.configurations = config
    component.install()

    server = Server(pidfile, stdin, stdout, stderr, directory, umask)
    server.set_app(Application(component.urls))
    server.set_port(config.get('port') or 9654)

    ctx.obj = {}
    ctx.obj['server'] = server
    ctx.obj['daemon'] = daemon



@main.command()
@click.pass_context
def start(ctx):
    """Start Blackgate."""
    if ctx.obj['daemon']:
        ctx.obj['server'].start()
    else:
        ctx.obj['server'].run()

@main.command()
@click.pass_context
def stop(ctx):
    """Stop Blackgate."""
    server = ctx.obj['server']
    server.stop()


@main.command()
@click.pass_context
def restart(ctx):
    """Restart Blackgate."""
    server = ctx.obj['server']
    server.restart()

@main.command()
@click.pass_context
def status(ctx):
    """Inspect Blackgate Status."""
    server = ctx.obj['server']
    server.is_running()



if __name__ == '__main__':
    main()
