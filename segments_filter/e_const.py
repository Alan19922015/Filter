#!/usr/bin/env python


import numpy as np
import sys
import fiona
import rasterio
from rasterio.tools.mask import mask

def main():
    if sys.argv[5]=='N':
        clip='clip_N.shp'
    elif sys.argv[5]=='S':
        clip='clip_S.shp'
    else:
        print 'Is it in the N(orth) or S(outh)?'
        exit
    with fiona.open(clip,'r') as shp:
        coords=[feature['geometry'] for feature in shp]
    with rasterio.open(sys.argv[1]) as src:
        clipped1, out_transform = mask(src,coords,nodata=np.nan,crop=False)
    with rasterio.open(sys.argv[2]) as src:
        clipped2, out_transform = mask(src,coords,nodata=np.nan,crop=False)


    sigma_c=(np.nanmedian(clipped1)+np.nanmedian(clipped2))/float(2)       # coregistration error
    if np.isnan(sigma_c):
        sigma_c=0
    #print 'sigma_c', sigma_c
    C=0.4                         # uncertainty of the tracking algorithm [p]
    delta_x=float(sys.argv[4])    # image resolution [m/p]
    delta_t=float(sys.argv[3])    # time interval between images [d]
    z=2                           # oversampling factor

    #### C and z values taken from Seehaus 2015 

    sigma_t=C*delta_x/float(z*delta_t)*365.2     # uncertainties in the velocity field due to the tracking algorithm
    #print 'sigma_t', sigma_t
    e_const=np.sqrt(sigma_t**2+sigma_c**2)
    print e_const

if __name__ == "__main__": main()
