#!/usr/bin/env python

from time import *
from netCDF4 import Dataset
import math
import numpy
import warnings
import filter
import sys
sys.setrecursionlimit(50000000)

###  usage: ./filter.py vx vy min_number e_const w prior_vx prior_vy


print("Computation of Rosenau filter started at", strftime("%a, %d %b %Y %H:%M:%S", localtime()))
t0=clock()
################## INPUT ##########################################################################################################
###  directories
dir_vx=sys.argv[1]                         ###  vx
dir_vy=sys.argv[2]                         ###  vx
dir_prior_vx=sys.argv[6]                   ###  prior vx
dir_prior_vy=sys.argv[7]                   ###  prior vy

###  reading nc-files
print '.....reading data.....'
vx_data=Dataset(dir_vx, mode='r')          ###  open files
vy_data=Dataset(dir_vy, mode='r')
prior_vx_data=Dataset(dir_prior_vx, mode='r')
prior_vy_data=Dataset(dir_prior_vy, mode='r')
if 'z' in vx_data.variables:
    z=vx_data.variables['z']                   ### save data in variables
elif 'Band1' in vx_data.variables:
    z=vx_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
vx=z[:,:]
if 'z' in vy_data.variables:
    z=vy_data.variables['z']                   ### save data in variables
elif 'Band1' in vy_data.variables:
    z=vy_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
vy=z[:,:]
if 'z' in prior_vx_data.variables:
    z=prior_vx_data.variables['z']                   ### save data in variables
elif 'Band1' in prior_vx_data.variables:
    z=prior_vx_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
prior_vx=z[:,:]
if 'z' in prior_vy_data.variables:
    z=prior_vy_data.variables['z']                   ### save data in variables
elif 'Band1' in prior_vy_data.variables:
    z=prior_vy_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
prior_vy=z[:,:]
if 'x' in vx_data.variables:
    hor=vx_data.variables['x']                ###  x-coordinates
elif 'lon' in vx_data.variables:
    hor=vx_data.variables['lon']
else:
    print 'Name of NetCDF variable not known.'
    exit
if 'y' in vx_data.variables:
    ver=vx_data.variables['y']                ###  y-coordinates
elif 'lat' in vx_data.variables:
    ver=vx_data.variables['lat']
else:
    print 'Name of NetCDF variable not known.'
    exit
vx_data.close()                           ###  close files
vy_data.close()
prior_vx_data.close()
prior_vy_data.close()

###  initialization
treat=set()                              ###  points which are already in a segment
start=set()                              ###  possible starting points
seg=[]                                   ###  points in actual segment
seg_list=[]                              ###  list of segments
min_number=sys.argv[3]                   ###  minimum number of elements in a segment
min_number=float(min_number)
min_number=numpy.sqrt(min_number**2)
dim=vx.shape                             ###  dimensions of the array
w=sys.argv[5]                                    ###  how much difference to prior-field is allowed (should be between 1 and 1.5)
w=float(w)
w=numpy.sqrt(w**2)
a=sys.argv[8]
a=float(a)
a=numpy.sqrt(a**2)
e_const=sys.argv[4]             ###  constant error term (includes coregistration and feature tracking)
e_const=float(e_const)
print e_const
e_const=numpy.sqrt(e_const**2)
e_const=a*e_const
col=numpy.zeros((dim[0],dim[1]))         ###  every segment gets another value (for colours)

print "Properties of Rosenau filter: "
print "minimum number of elements in a segment:", min_number
print "dimensions of the array:", dim
print "constant error term (includes coregistration and feature tracking):", e_const
print "how much difference to prior-field is allowed (should be between 1 and 1.5)", w

########  FUNCTIONS  ##############################################################################################################
def new_segment(new_s,all_s):
    """Appends new segment to list of segments and returns it"""
    all_s.append(new_s)
    return all_s
 

########  MAIN  ###################################################################################################################

v=(0,0)
start.add(v)
   
while len(start) !=0:                              ###  recursive gradient approach
        p=start.pop()
        if not math.isnan(vx[p]) and not math.isnan(vy[p]):
            seg.append(p)
	filter.rekgrad(p[0],p[1],treat,seg,start,dim,vx,vy,prior_vx,prior_vy,w,e_const)
	if seg!=[]:
            seg_list=new_segment(seg,seg_list)
            seg=[]
            
print "all points treated"
k=0
for i in xrange(0, len(seg_list)):
    k=k+1
    for j in seg_list[i]:
        col[j]=k
	if len(seg_list[i])<min_number:       ### delete segments with less than min_number elements
	    vx[j]=numpy.nan
            vy[j]=numpy.nan



#######  WRITING NC-FILES  ########################################################################################################
print '.....writing data.....'
vx_data=Dataset(dir_vx,'a')                        ###  open file
if 'z' in vx_data.variables:
    z=vx_data.variables['z']                   ### save data in variables
elif 'Band1' in vx_data.variables:
    z=vx_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
z[:,:]=vx                                          ###  save data
vx_data.close()                                    ###  close file


vy_data=Dataset(dir_vy,'a')                        ###  open file
if 'z' in vy_data.variables:
    z=vy_data.variables['z']                   ### save data in variables
elif 'Band1' in vy_data.variables:
    z=vy_data.variables['Band1']
else:
    print 'Name of NetCDF variable not known.'
    exit
z[:,:]=vy                                          ###  save data
vy_data.close()                                    ###  close file



t1=clock()                                         ###  computation time
t=t1-t0
print "computation time:", t
