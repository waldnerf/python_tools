# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:24:45 2014

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
    

def rasterizeToTargetGrid(inShp, outRst, targetRst,className, dt):
    import os
    import osr, gdal
    
    # Get target srs
    gdal.AllRegister()
    Ds = gdal.Open(targetRst,gdal.GA_ReadOnly)
    projWKT = Ds.GetProjection()
    
    srs = osr.SpatialReference()
    srs.ImportFromWkt(projWKT)                  
    target_srs = srs.ExportToProj4()
    
    from osgeo import ogr, osr
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(inShp)
    
    # from Layer
    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()
    input_srs = spatialRef.ExportToProj4() 
    
    
    if target_srs != input_srs:
        outShp = inShp.split('.shp')[0]+'_reproj.shp'
        ogr2ogr = 'ogr2ogr -t_srs "%s" %s %s'%(target_srs, outShp, inShp)    
        os.system(ogr2ogr)
        inShp = outShp
    
    # Get target extent and resotution
    [xmin, ymin, xmax, ymax, xres, yres] = getBoundingBox(targetRst)
    
    rasterize = 'gdal_rasterize -a %s -ot %s -te %s %s %s %s -tr %s %s -a_nodata "-99" -co "COMPRESS=LZW" -co "TILED=YES" -l %s %s %s'%(className, dt, xmin, ymin, xmax, ymax, xres, abs(yres), (inShp.split('.shp')[0]).split('/')[-1], inShp, outRst)
    print(rasterize)    
    os.system(rasterize)
    return 'rasterizeToTargetGrid ok'

	
if __name__ == '__main__':
    import sys
    inShp     = sys.argv[0]
	outRst    = sys.argv[1]
    targetRst    = sys.argv[2]
    field    = sys.argv[3]
	dt    = sys.argv[4]
    rasterizeToTargetGrid(inShp, outRst, targetRst,field, dt)
