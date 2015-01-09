import gribnormalize as gribnorm

def upwrap_raster(input, output):
    import rasterio
    with rasterio.drivers():
        with rasterio.open(input, 'r') as src:
            fixedArrays = list(gribnorm.handleArrays(i) for i in src.read())
            fixAff, bounds = gribnorm.updateBoundsAffine(src.affine)
        print fixAff
        with rasterio.open(output, 'w',
            driver='GTiff',
            count=src.count,
            dtype=src.meta['dtype'],
            height=src.shape[0] * 2,
            width=src.shape[1] * 2,
            affine=fixAff
            ) as dst:
            for i, b in enumerate(fixedArrays):
                dst.write_band(i + 1, b)