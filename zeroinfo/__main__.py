# -*- coding: utf-8 -*-
"""Main script."""

import argparse
import asyncio
import click
import logging

from .__init__ import __version__
from .client import Client
from .server import Server


log = logging.getLogger('zeroinfo')


def print_version(ctx, param, value):
    """Prints the application version."""

    if not value or ctx.resilient_parsing:
        return

    print(__version__)
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def run():
    """Runs the application."""

    loop = asyncio.get_event_loop()

    server = Server(loop)
    server.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()


@click.group()
@click.option('--version',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help='Print version and exit.')
def cli():
    """Command line entry point."""
    pass

@cli.command()
def server():
    """Run the server."""

    print('Press CTRL+C to exit...')
    loop = asyncio.get_event_loop()

    server_instance = Server(loop)
    server_instance.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()

@cli.command()
def client():
    """Run the server."""

    print('Press CTRL+C to exit...')
    loop = asyncio.get_event_loop()

    client_instance = Client(loop)
    client_instance.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()

if __name__ == '__main__':
    cli()
