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

    return outAffine, bounds


def doThis(yo, hey):
    import click
    for i in range(hey):
        click.echo(yo)