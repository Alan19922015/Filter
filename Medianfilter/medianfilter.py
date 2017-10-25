#!/usr/bin/env python
from __future__ import print_function
from time import *
import math
from netCDF4 import Dataset
import numpy as np
import sys
import medianfilter

###  usage: python medianfilter.py $1 $2 $3 $4 $5 $6
###  $1: vx input
###  $2: vy input
###  $3: vx output
###  $4: vy output
###  $5: chipsize
###  $6: eps
t1=clock()
print("Computation of median filter started at", strftime("%a, %d %b %Y %H:%M:%S", localtime()))


def write(vx,vy,dvx,dvy,chipsize,epsilon):
        """Writing computed data in one nc-file"""
        print(".....writing data.....")

        vx_data=Dataset(dvx,'a')                        ###  open file
        if 'z' in vx_data.variables:
                z=vx_data.variables['z']                   ### save data in variables
        elif 'Band1' in vx_data.variables:
                z=vx_data.variables['Band1']
        else:
                print('Name of NetCDF variable not known.')
                exit
        z[:,:]=vx                                          ###  save data
        vx_data.close()

        vy_data=Dataset(dvy,'a')                        ###  open file
        if 'z' in vy_data.variables:
                z=vy_data.variables['z']                   ### save data in variables
        elif 'Band1' in vy_data.variables:
                z=vy_data.variables['Band1']
        else:
                print('Name of NetCDF variable not known.')
                exit
        z[:,:]=vy                                          ###  save data
        vy_data.close()
 
def read(dvx,dvy):
        """Reading data from nc-files"""
        print(".....reading data.....")
        
        vx_data=Dataset(dvx, mode='r')          ###  open files
        vy_data=Dataset(dvy, mode='r')
        if 'z' in vx_data.variables:
                z=vx_data.variables['z']                   ### save data in variables
        elif 'Band1' in vx_data.variables:
                z=vx_data.variables['Band1']
        else:
                print('Name of NetCDF variable not known.')
                exit
        vx=z[:,:]
        if 'z' in vy_data.variables:
                z=vy_data.variables['z']                   ### save data in variables
        elif 'Band1' in vy_data.variables:
                z=vy_data.variables['Band1']
        else:
                print('Name of NetCDF variable not known.')
                exit
        vy=z[:,:]
        vx_data.close()                           ###  close files
        vy_data.close()
        return(vx,vy)




def printing(m,n,cs,eps):
    print("______Preferences:_____")
    print("dimensions:",(m,n))
    print("chipsize:",cs)
    print("eps*std:",eps)


def main():

       (vx,vy)=read(sys.argv[1],sys.argv[2])                       
       cs=sys.argv[5]
       cs=float(cs)
       cs=np.sqrt(cs**2)
       if cs>vx.shape[0] or cs>vx.shape[1]:
               print('chipsize greater than dimensions of the array')
               exit
       eps=sys.argv[6]
       eps=float(eps)
       eps=np.sqrt(eps**2)
       printing(vx.shape[0],vx.shape[1],cs,eps)
       (nx,ny)=medianfilter.f(vx,vy,cs,eps)
       write(nx,ny,sys.argv[3],sys.argv[4],cs,eps)




if __name__ == "__main__": main()

t2=clock()
print("Computation time:",t2-t1)
