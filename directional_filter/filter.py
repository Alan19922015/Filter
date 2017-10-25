#!/usr/bin/env python
from __future__ import print_function
from time import *
import math
from netCDF4 import Dataset
import numpy as np
import sys

###  usage: python medianfilter.py $1 $2 $3 $4 $5 $6
###  $1: vx input
###  $2: vy input
###  $3: mask output
###  $4: angle
###  $5: chipsize
###  $6: e

t1=clock()

def write(vx,dvx,chipsize,error_angle,mean_error):
        """Writing computed data new nc-file which is a mask"""
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



 
def neighbours(x,y,m,n):
        """Gives for given point (x,y) and dimensions of matrix m,n the list of neighbours: [(x1,y1) ... (xa,ya)]"""
        if x>m:
    	        print("Error: in filter.py, neighbors((x,y),m,n): x=",x, "exceeds dimension m =", m)
    	        exit()
        elif y>n:
    	        print("Error: in filter.py, neighbors((x,y),m,n): y=",y, "exceeds dimension n =", n)
    	        exit()
        l=[]
        if x==0:
                if y==0:
                        l.append((x+1,y))
                        l.append((x,y+1))
                        l.append((x+1,y+1))
                elif y==n:
                        l.append((x,y-1))
                        l.append((x+1,y))
                        l.append((x+1,y-1))

                else:
                        l.append((x+1,y))
                        l.append((x,y-1))
                        l.append((x,y+1))
                        l.append((x+1,y-1))
                        l.append((x+1,y+1))
        elif x==m:
    	        if y==0:
                        l.append((x-1,y))
                        l.append((x,y+1))
                        l.append((x-1,y+1))
                elif y==n:
                        l.append((x,y-1))
                        l.append((x-1,y))
                        l.append((x-1,y-1))

                else:
                        l.append((x,y+1))
                        l.append((x,y-1))
                        l.append((x-1,y))
                        l.append((x-1,y-1))
                        l.append((x-1,y+1))
    	
        else:
    	        if y==0:
                        l.append((x-1,y))
                        l.append((x+1,y))
                        l.append((x-1,y+1))
                        l.append((x,y+1))
                        l.append((x+1,y+1))
                elif y==n:
                        l.append((x-1,y))
                        l.append((x+1,y))
                        l.append((x-1,y-1))
                        l.append((x,y-1))
                        l.append((x+1,y-1))

                else:
                        l.append((x,y+1))
                        l.append((x,y-1))
                        l.append((x-1,y))
                        l.append((x-1,y-1))
                        l.append((x-1,y+1))
                        l.append((x+1,y))
                        l.append((x+1,y-1))
                        l.append((x+1,y+1))
        return l


def printing(m,n,s,e,r):
    print("______Preferences:_____")
    print("dimensions:",(m,n))
    print("maximum error angle:",s)
    print("maximum error from mean:",e,"*std")
    print("chipsize for computing mean:",r)



def filtering(r,ri,e,s):
        m=ri.shape[0]
        n=ri.shape[1]
        for i in xrange(0,m):
                for j in xrange(0,n):
                        if not math.isnan(ri[i,j]):
                                [me,std]=mean(ri,i,j,r)
                                print(ri[i,j], me,std, e*std)                                
                                if ri[i,j]<me-e*std or ri[i,j]>me+e*std:
                                        ri[i,j]=np.nan
                                        print("removed by window")
                                nb=neighbours(i,j,m-1,n-1)
                                z=0
                                nan=0
                                for k in nb:
                                        if not math.isnan(ri[k]):
                                                if abs(ri[i,j]-ri[k])>s:
                                                        z=z+1
                                                        if z==5:
                                                                ri[i,j]=np.nan
                                                                z=0
                                                                print("removed by angle")
                                                                break
                                        else:
                                                nan=nan+1
                                                if nan>=len(nb)-2:
                                                        ri[i,j]=np.nan
                                                        print("removed by nan")
                                                        break
        return ri


def mean(mat,k,l,cs):
        if k-(cs/2)<0:
                b1=0
                b2=cs
        elif k+(cs/2)>mat.shape[0]:
                b2=mat.shape[0]
                b1=mat.shape[0]-cs
        else:
                b1=k-cs/2
                b2=k+cs/2  
        if l-(cs/2)<0:
                b3=0
                b4=cs
        elif l+(cs/2)>mat.shape[1]:
                b4=mat.shape[1]
                b3=mat.shape[1]-cs
        else:
                b3=l-cs/2
                b4=l+cs/2
        hmat=[]
        for i in xrange(b1,b2):
                for j in xrange(b3,b4):
#                        print(mat[i,j])
                        if not math.isnan(mat[i,j]):
                                hmat.append(mat[i,j])
        np_hmat=np.array(hmat)
        return(np.mean(np_hmat),np.std(np_hmat)) 
                




def main():
########VARIABLES##########################################################################################################
    (dvx,dvy)=read(sys.argv[1],sys.argv[2])
    drc=np.arccos(dvx/np.sqrt(dvx**2+dvy**2))
#    for i in range(drc.shape[0]):
#        for j in range(drc.shape[1]):
#                print(drc[i,j], dvx[i,j], dvy[i,j])
    m1=drc.shape[0]
    n1=drc.shape[1]
    angle=sys.argv[4]
    angle=float(angle)
    angle=np.sqrt(angle**2)
    s1=(math.pi/float(180))*angle
    e1=sys.argv[6]
    e1=float(e1)
    e1=np.sqrt(e1**2)
    r1=sys.argv[5]
    r1=float(r1)
    r1=np.sqrt(r1**2)
    r1=int(r1)
    if r1>drc.shape[0] or r1>drc.shape[1]:
               print('chipsize greater than dimensions of the array! Set to r1=',min(drc.shape))
               r1=min(drc.shape)
    printing(m1,n1,s1,e1,r1)
    back=filtering(r1,drc,e1,s1)
    write(back,sys.argv[3],r1,s1,e1)
    return 1



if __name__ == "__main__": main()

t2=clock()
print("Computation time:",t2-t1)
