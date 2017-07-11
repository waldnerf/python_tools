# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 18:08:23 2014

@author: waldner
"""
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
    
    return xmin, ymin, xmax, ymax, xres, yres 

def resample2grid(inRst, targetRst, outRst,mtd='near',dt='Int16'):
    import os
    import osr, gdal
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
    return('done')

if __name__ == '__main__':
    import sys
    inRst     = sys.argv[0]
    targetRst = sys.argv[1]
    outRst    = sys.argv[2]
    outRst    = sys.argv[3]
    outRst    = sys.argv[4]
    resample2grid(inRst, targetRst, outRst,mtd='near',dt='Int16')
