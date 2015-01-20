import cut_splice_globewrap as csg, click

@click.group()
def cli():
    pass

@click.command('unwrap')
@click.argument('inputgrib', type=str)
@click.argument('output', type=str)
@click.option('--bidx', '-b', default='all',
    help='Bands to include [default = all]')
@click.option('--bandtags', '-bt', is_flag=True,
    help='Flag to indicate printing of band tags / band metadata to stdout')
def unwrap(inputgrib, output, bidx, bandtags):
    csg.upwrap_raster(inputgrib, output, bidx, bandtags)

cli.add_command(unwrap)