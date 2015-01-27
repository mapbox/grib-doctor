import cut_splice_globewrap as csg, click

@click.group()
def cli():
    pass

@click.command('unwrap')
@click.argument('inputgrib', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
@click.option('--bidx', '-b', default='all',
    help='Bands to include [default = all]')
@click.option('--bandtags', '-bt', is_flag=True,
    help='Flag to indicate printing of band tags / band metadata to stdout')
def unwrap(inputgrib, output, bidx, bandtags):
    csg.upwrap_raster(inputgrib, output, bidx, bandtags)

cli.add_command(unwrap)

@click.command('smoosh')
@click.argument('inputs', type=click.Path(exists=True), nargs=-1)
@click.argument('output', type=click.Path(exists=False), nargs=1)
def smoosh(inputs, output):
    'stack multiple global gfs gribs of (possible) varying resolutions'
    csg.smoosh_rasters(inputs, output)

cli.add_command(smoosh)