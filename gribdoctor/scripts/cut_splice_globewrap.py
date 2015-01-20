import gribdoctor
import click, json, numpy as np

def upwrap_raster(inputRaster, outputRaster, bidx, bandtags):
    import rasterio

    with rasterio.drivers():
        with rasterio.open(inputRaster, 'r') as src:
            if bidx == 'all':
                bandNos = np.arange(src.count) + 1
            else:
                bandNos = list(int(i.replace(' ', '')) for i in bidx.split(','))

            fixedArrays = list(gribdoctor.handleArrays(src.read_band(i)) for i in bandNos)

            fixAff, bounds = gribdoctor.updateBoundsAffine(src.affine)
            if bandtags:
                tags = list(src.tags(i + 1) for i in range(src.count))
                click.echo(json.dumps(tags, indent=2))

        with rasterio.open(outputRaster, 'w',
            driver='GTiff',
            count=src.count,
            dtype=src.meta['dtype'],
            height=src.shape[0] * 2,
            width=src.shape[1] * 2,
            transform=fixAff,
            crs=src.crs
            ) as dst:
            for i, b in enumerate(fixedArrays):
                dst.write_band(i + 1, b)