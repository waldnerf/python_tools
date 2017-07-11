# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:12:46 2016

@author: waldner
"""

from osgeo import gdal
import gdal
from gdalconst import *
import sys,os 
import optparse
import operator
gdal.AllRegister()

def processDataset(src_file, dst_dir, tilesize, compression):
    """ 
    Much of the code in this function relating to reading and writing gdal
    datasets - especially reading block by block was acquired from
    Chris Garrard's Utah State Python Programming GIS slides:
        http://www.gis.usu.edu/~chrisg/
    """

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    out_file = os.path.join(dst_dir, os.path.splitext(os.path.basename(src_file))[0])

    src_ds = gdal.Open(src_file)
    if src_ds is None:
        print 'Could not open image'
        sys.exit(1)
    width = src_ds.RasterXSize
    height = src_ds.RasterYSize
    
    print width, 'x', height
    for i in range(0, width, tilesize):
       for j in range(0, height, tilesize):
            w = min(i+tilesize, width) - i
            h = min(j+tilesize, height) - j
            gdaltranString = "gdal_translate -of GTIFF -srcwin "+str(i)+", "+str(j)+", "+str(w)+", " +str(h)+" " + src_file + " " + out_file + "_"+str(i)+"_"+str(j)+".tif  -co "+compression+" -co TILED=YES -co BIGTIFF=YES --config GDAL_CACHEMAX 4000"
            os.system(gdaltranString)
    src_ds = None


def main():
    p = optparse.OptionParser()
    p.add_option('--ts', '-t', default='1000', help = ("Tile size"
        " The default is '1'"))
    p.add_option('--compress_method', '-p', default='COMPRESS=NONE', help=("GDAL compression"
        " method. Examples:'COMPRESS = LZW','COMPRESS = PACKBITS','COMPRESS = DEFLATE' or "
        "'COMPRESS = JPEG'. The default is no compression."))
    options, arguments = p.parse_args()
    
    
    src_file, dst_dir = arguments[0], arguments[1]
    
    tilesize = int(options.ts)
    compression = options.compress_method

    if len([src_file, dst_dir, tilesize]) == 3:
        processDataset(src_file, dst_dir, tilesize, compression)
    else:
        print "Provide enough input."

if __name__ == '__main__':
    main()