#-*-python-*-
from __future__ import print_function
from time import *
import math
from netCDF4 import Dataset
import numpy as np
import sys
import math
import numpy.ma as ma

def f(x,y,c,e):
        m=x.shape[0]
        n=x.shape[1]
        z=0
        x=ma.array(x)
        y=ma.array(y)
        x.mask=ma.nomask
        y.mask=ma.nomask
        for i in xrange(0,m):
                for j in xrange(0,n):
                        z=z+1
                        if not math.isnan(x[i,j]):
                                (m1,m2,s1,s2)=median_std(x,y,i,j,c,z)
                                if math.isnan(m1) or math.isnan(m2) or math.isnan(s1) or math.isnan(s2):
                                        x[i,j]=np.nan
                                        y[i,j]=np.nan
                                if x[i,j]<m1-e*s1 or x[i,j]>m1+e*s1 or y[i,j]<m2-e*s2 or y[i,j]>m2+e*s2:
                                        x[i,j]=np.nan
                                        y[i,j]=np.nan
        return(x,y)


def median_std(x,y,i,j,c,index):
        if i-(c/2)<0:
                b1=0
                b2=c
        elif i+(c/2)>x.shape[0]:
                b2=x.shape[0]
                b1=x.shape[0]-c
        else:
                b1=i-c/2
                b2=i+c/2
                
        if j-(c/2)<0:
                b3=0
                b4=c
        elif j+(c/2)>x.shape[1]:
                b4=x.shape[1]
                b3=x.shape[1]-c
        else:
                b3=j-c/2
                b4=j+c/2
        
        b1 = int(b1)
        b2 = int(b2)
        b3 = int(b3)
        b4 = int(b4)        
        med1=np.nanmedian(x[b1:b2,b3:b4])
        med2=np.nanmedian(y[b1:b2,b3:b4])
        std1=np.nanstd(x[b1:b2,b3:b4])
        std2=np.nanstd(y[b1:b2,b3:b4])
        return(med1,med2,std1,std2)    
    

