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

            fixAff = gribdoctor.updateBoundsAffine(src.affine)
            if bandtags:
                tags = list(src.tags(i + 1) for i in range(src.count))
                click.echo(json.dumps(tags, indent=2))

        with rasterio.open(outputRaster, 'w',
            driver='GTiff',
            count=len(bandNos),
            dtype=src.meta['dtype'],
            height=src.shape[0] * 2,
            width=src.shape[1] * 2,
            transform=fixAff,
            crs=src.crs
            ) as dst:
            for i, b in enumerate(fixedArrays):
                dst.write_band(i + 1, b)

def smoosh_rasters(inputRasters, outputRaster):
    import rasterio

    rasInfo = list(gribdoctor.loadRasterInfo(b) for b in inputRasters)

    snapShape = gribdoctor.getSnapDims(rasInfo)

    snapSrc = gribdoctor.getSnapAffine(rasInfo, snapShape)

    allBands = list(gribdoctor.loadBands(b, snapShape) for b in inputRasters)

    with rasterio.drivers():
        with rasterio.open(outputRaster, 'w',
            driver='GTiff',
            count=len(allBands),
            dtype=snapSrc['dtype'],
            height=snapShape[0] * 2,
            width=snapShape[1] * 2,
            transform=snapSrc['affine'],
            crs=snapSrc['crs']
            ) as dst:
            for i, b in enumerate(allBands):
                dst.write_band(i + 1, b)