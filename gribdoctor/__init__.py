def handleArrays(gribArr):
    import numpy as np
    from scipy.ndimage import zoom

    gribArr = zoom(gribArr, 2, order=1)
    oshape = gribArr.shape
    fixGrib = np.hstack((gribArr[:, oshape[1] / 2 + 1:oshape[1]],gribArr[:, 0:oshape[1] / 2 + 1]))

    return fixGrib

def updateBoundsAffine(inAffine):
    from rasterio import Affine, coords

    bounds = coords.BoundingBox(
        inAffine.c - 180.0 + (inAffine.a / 2.0),
        -inAffine.f,
        -(inAffine.c - 180.0 + (inAffine.a / 2.0)),
        inAffine.f)

    outAffine = Affine(inAffine.a / 2.0, inAffine.b,inAffine.c - 180.0 + (inAffine.a / 2.0),
         inAffine.d,inAffine.e / 2.0, inAffine.f)

    return outAffine

def loadRasterInfo(inputRaster):
    import rasterio
    with rasterio.open(inputRaster, 'r') as src:
        return {
            'shape': src.shape,
            'affine': src.affine,
            'dtype': src.meta['dtype'],
            'crs': src.crs
        }

def getSnapDims(rasInfo):
    snapRows = max(list(
        i['shape'][0] for i in rasInfo
    ))

    snapCols = max(list(
        i['shape'][1] for i in rasInfo
    ))

    return (snapRows, snapCols)

def getSnapAffine(rasInfo, snapshape):
    rasMap = {i['shape']: {
        'affine': updateBoundsAffine(i['affine']),
        'dtype': i['dtype'],
        'crs': i['crs']
        } for i in rasInfo}
    return rasMap[snapshape]


def loadBands(inputRaster, snapshape):
    import rasterio
    import numpy as np
    from scipy.ndimage import zoom

    with rasterio.drivers():
        with rasterio.open(inputRaster, 'r') as src:
            if src.count == 1:
                data = src.read_band(1)
                try:
                    data[np.where(data.mask == True)] = data.min()
                except AttributeError:
                    pass
                if data.shape != snapshape:
                    data = handleArrays(data)
                    data = zoom(data, 2 * snapshape[1] / data.shape[1], order=1)
                    data = ((np.roll(data, 1, axis=0) + data) / 2)[1:]

                else:
                    data = handleArrays(data)

                return data
            else:
                return list(src.read())