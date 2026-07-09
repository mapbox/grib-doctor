import gribdoctor
import click, json, numpy as np

def upwrap_raster(inputRaster, outputRaster, bidx, bandtags):
    import rasterio
    import rasterio.env

    with rasterio.Env():
        with rasterio.open(inputRaster, 'r') as src:
            print(src)
            if bidx == 'all':
                bandNos = np.arange(src.count) + 1
            else:
                bandNos = list(int(i.replace(' ', '')) for i in bidx.split(','))

            fixedArrays = list(gribdoctor.handleArrays(src.read(i)) for i in bandNos)

            fixAff = gribdoctor.updateBoundsAffine(src.transform)
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

def smoosh_rasters(inputRasters, outputRaster, gfs, development):
    import rasterio
    import rasterio.env
    import numpy as np
    
    # if isinstance(inputRasters, list):
    #     pass
    # else:
    #     inputRasters = [inputRasters]

    rasInfo = list(gribdoctor.loadRasterInfo(b) for b in inputRasters)
    
    if abs(rasInfo[0]['affine'].c) > 360 and development == True:
        gfs = False
        kwargs = rasInfo[0]['kwargs']
    elif development == True:
        gfs = True

    snapShape = gribdoctor.getSnapDims(rasInfo)
    snapSrc = gribdoctor.getSnapAffine(rasInfo, snapShape)

    allBands = list(gribdoctor.loadBands(b, snapShape, gfs) for b in inputRasters)
    
    allBands = list(b for sub in allBands for b in sub)

    if gfs:
        zoomFactor = 2
        kwargs = gribdoctor.makeKwargs(allBands, snapSrc, snapShape, zoomFactor)
    else:
        zoomFactor = 1
        kwargs['count'] = len(allBands)
        kwargs['driver'] = 'GTiff'

    with rasterio.Env():
        with rasterio.open(outputRaster, 'w', **kwargs) as dst:
            for i, b in enumerate(allBands):
                dst.write_band(i + 1, b)
