# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:51:42 2017

@author: waldner
"""
import sys
import os
import osr
import optparse
import operator
from osgeo import gdal
import gdal
from gdalconst import *

def getBoundingBox(inRst):
    import gdal
    ds = gdal.Open(inRst, 0)
    if ds is None:
        print 'Could not open ' + inRst
        sys.exit(1)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    geotransform = ds.GetGeoTransform()
    
    xmin = geotransform[0]
    ymax = geotransform[3]
    
    xres  = geotransform[1]
    yres = geotransform[5]
    
    xmax = xmin+cols*xres
    ymin = ymax+rows*yres
    ds = None
    return xmin, ymin, xmax, ymax, xres, yres 

def resample2grid(inRst, targetRst, outRst,mtd='near',dt='Int16'):

    # Get target srs
    gdal.AllRegister()
    Ds = gdal.Open(targetRst,gdal.GA_ReadOnly)
    projWKT = Ds.GetProjection()
    
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projWKT)                  
    target_srs = srs.ExportToProj4()
    
    # Get target extent and resotution
    [xmin, ymin, xmax, ymax, xres, yres] = getBoundingBox(targetRst)
    
    inDs = gdal.Open(inRst, 1)
    if inDs is None:
      print 'Could not open', inRst
      sys.exit(1)
    driver = inDs.GetDriver()
    inBand = inDs.GetRasterBand(1)
    naVal = inBand.GetNoDataValue()
    
    warp = "gdalwarp -ot %s -t_srs '%s' -te %s %s %s %s -tr %s %s -r %s -srcnodata '%s' -dstnodata '%s' -overwrite -multi -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=YES --config GDAL_CACHEMAX 4000 %s %s"%(dt,target_srs,xmin, ymin, xmax, ymax, xres, abs(yres),mtd, naVal,naVal, inRst, outRst )
    os.system(warp)
    inBand = None    
    inDs = None
    return('done')

def main():
    p = optparse.OptionParser()
    p.add_option('--ts', '-t', default='1000', help = ("Tile size"
        " The default is '1'"))
    p.add_option('--resampling_method', '-r', default='near', help=("GDAL resampling method"))
    options, arguments = p.parse_args()
    
    inRst     = arguments[0]
    targetRst = arguments[1]
    outRst    = arguments[2]
    
    resampling = (options.resampling_method)


    if len([inRst, targetRst, outRst]) == 3:
        resample2grid(inRst, targetRst, outRst,mtd=resampling,dt='Int16')
    else:
        print "Provide enough input."

if __name__ == '__main__':
    main()


    