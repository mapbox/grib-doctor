gribdoctor
==========

Utility functions for handling quirks of weather data rasters in `grib2` format

Usage - unwrap
--------------

.. role:: console(code)
   :language: console

:console:`gribdoctor unwrap [OPTIONS] INGRIB OUTRASTER`

OPTIONS

- :console:`-bt, --bandtags  Flag to indicate printing of band tags / band metadata to stdout`

- :console:`-b, --bidx  Bands to include in output raster. Default = all (use caution - you may inadvertently create ginourmous tif files)`

Many gridded weather GRIBs, such as NOAA's `Global Forecast System (GFS) <http://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>`_, cover a global extent of -0.5 to 359.5 (or similar, depending on resolution), with the antimeridian (-180 / 180) bisecting a column of pixels.
This routine upsamples, slices, and merges these rasters as to convert them to "standard" -180 to 180 extent global grids. Outputs to any raster format supported by `rasterio <https://github.com/mapbox/rasterio>`_.
