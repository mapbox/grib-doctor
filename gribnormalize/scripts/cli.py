# Skeleton of a CLI

import click

import gribnormalize


@click.command('gribnormalize')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(gribnormalize.has_legs)
