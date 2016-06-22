# -*- coding: utf-8 -*-

import click

from blackgate.core import component
from blackgate.server import run

@click.group()
def main():
    # README CONFIG
    component.install_from_config(config)

@main.command()
def start():
    run(config.get('port', 9654))


if __name__ == '__main__':
    main()
