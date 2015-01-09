import click
import cut_splice_globewrap as csg

@click.group()
def cli():
    pass

@click.command('unwrap')
@click.argument('inputgrib', type=str)
@click.argument('output', type=str)
def unwrap(inputgrib, output):
    csg.upwrap_raster(inputgrib, output)

cli.add_command(unwrap)