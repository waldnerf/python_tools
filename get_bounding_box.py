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
    
    return xmin, ymin, xmax, ymax

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    getBoundingBox()