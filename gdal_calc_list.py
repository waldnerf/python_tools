# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:12:46 2016

Recursive calc operation on a list of rasters

@author: waldner
"""

from osgeo import gdal
import gdal
from gdalconst import *
import sys,os 
import optparse
import operator
gdal.AllRegister()

def processDataset(src_files, dst_file, calc):

    src_file_a = src_files[0]
    dst_dir = os.path.dirname(dst_file)    
    
    for src_file in src_files[1:]:
        src_file_b = src_file
        outfile  = os.path.join(dst_dir, os.path.basename(src_file_b).split('.tif')[0]+'_tempfile.tif')
        gdalcalc = 'gdal_calc.py -A '+ src_file_a + ' -B '+ src_file_b + ' --outfile='+outfile+' --calc="'+calc+'" --co="COMPRESS=LZW" --co="TILED=YES" --overwrite'                 
        os.system(gdalcalc)   

        if '_tempfile.tif' in src_file_a:
            gdalmanage = 'gdalmanage delete %s'%(src_file_a)
            os.system(gdalmanage)        
        
        src_file_a = outfile
        
        
    
    gdalmanage = 'gdalmanage copy %s %s'%(outfile, dst_file)
    os.system(gdalmanage)
    
    gdalmanage = 'gdalmanage delete %s'%(outfile)
    os.system(gdalmanage)


def main():
    p = optparse.OptionParser()
    p.add_option('--calc', '-c', default='A+B', help = ("Calc function"
        " The default is 'A+B'"))
    options, arguments = p.parse_args()
    
    
    dst_file, src_files = arguments[0], arguments[1:]
    calc = (options.calc)

    if len([src_files, dst_file]) >= 2:
        processDataset(src_files, dst_file, calc)
    else:
        print "Provide enough input."

if __name__ == '__main__':
    main()