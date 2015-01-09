import click
import cut_splice_globewrap as csg

@click.group()
def cli():
    pass

@click.command('unwrap')
@click.argument('inputgrib', type=str)
@click.argument('output', type=str)
@click.option('--bandtags', '-bt', is_flag=True,
    help='Flag to indicate printing of band tags / band metadata to stdout')
def unwrap(inputgrib, output, bandtags):
    csg.upwrap_raster(inputgrib, output, bandtags)

cli.add_command(unwrap)