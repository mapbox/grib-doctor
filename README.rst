gribdoctor
==========

Utility functions for handling quirks of weather data rasters in `grib2` format

Installation
-------
.. role:: console(code)
   :language: console
Using Anaconda w/ py38 env on Ubuntu x64
:console:`conda install gdal` (gdal 3.0.2)
:console:`pip install rasterio` (rasterio 1.1.2)
:console:`git clone https://github.com/laterdude/grib-doctor.git && cd ./grib-doctor && python -m setup install --force`

you may find memory issues occur w/ numpy arrays, if 
:console:`$ cat /proc/sys/vm/overcommit_memory`
:console:`0`
then as root run:
:console:`$ echo 1 > /proc/sys/vm/overcommit_memory`

Usage - smoosh
--------------

stack multiple gribs of the same or varying resolutions

:console:`Usage: gribdoctor smoosh [OPTIONS] [INPUTS]... OUTPUT`

OPTIONS:

:console:`-dev, --develoment  Dev tag for experimental features`

:console:`-uw, --unwrap       Unwrap GFS Rasters`

:console:`--help              Show this message and exit.`

Use this subcommand to "smoosh" together any number of variable resolution gribs into one tiff. This also effectively performs the below :console:`globewrap` operation on all inputs if indicated with :console:`--unwrap`, and outputs a raster of 2x (due to unwrapping) the highest input resolution.

Usage - unwrap
--------------

:console:`gribdoctor unwrap [OPTIONS] INGRIB OUTRASTER`

OPTIONS

:console:`-bt, --bandtags  Flag to indicate printing of band tags / band metadata to stdout`

:console:`-b, --bidx  Bands to include in output raster. Default = all (use caution - you may inadvertently create ginourmous tif files)`

Many gridded weather GRIBs, such as NOAA's `Global Forecast System (GFS) <http://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>`_, cover a global extent of -0.5 to 359.5 (or similar, depending on resolution), with the antimeridian (-180 / 180) bisecting a column of pixels.
This routine upsamples, slices, and merges these rasters as to convert them to "standard" -180 to 180 extent global grids. Outputs to any raster format supported by `rasterio <https://github.com/mapbox/rasterio>`_.
