import gribnormalize as gribnorm

def upwrap_raster(inputRas, output):
    import rasterio
    from rasterio import crs
    with rasterio.drivers():
        with rasterio.open(inputRas, 'r') as src:
            ## Upsamples by zooming, slices array at the dateline, and stitches array to make a -180 to 180 extent array
            fixedArrays = list(gribnorm.handleArrays(i) for i in src.read())
            fixAff, bounds = gribnorm.updateBoundsAffine(src.affine)

        with rasterio.open(output, 'w',
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