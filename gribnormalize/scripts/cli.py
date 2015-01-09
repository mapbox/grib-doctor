import click

import fliparr

@click.group()
def cli():
    pass

@click.command('unwrap')
@click.argument('ingrib', type=str)
@click.argument('outraster', type=str)
def unwrap(ingrib, outraster):
    fliparr.upwrap_raster(ingrib, outraster)

cli.add_command(unwrap)
