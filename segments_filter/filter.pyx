#-*-python-*-
import math
import numpy


def threshold(x,y,a,b,prior_vx,prior_vy,w,e_const):
        """Gives threshold of gradient in point (x,y) to point (a,b): threshold= e_const + w * difference between (x,y) and (a,b) in a-priori-field"""
        tx=abs((prior_vx[x,y]-prior_vx[a,b])*w)+e_const
        ty=abs((prior_vy[x,y]-prior_vy[a,b])*w)+e_const
        return (tx,ty)

def gradients(x1,y1,x2,y2,vx,vy):
        """Gives difference of vx and vy of points (x1,y1) and (x2,y2)"""
        return (vx[x1,y1]-vx[x2,y2],vy[x1,y1]-vy[x2,y2])



def neighbours(x,y,m,n):
        """Gives for given point (x,y) and dimensions of matrix m,n the list of neighbors: [(x1,y1) ... (xa,ya)]"""

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


def rekgrad(x,y,treat,seg,start,dim,vx,vy,prior_vx,prior_vy,w,e_const):
        treat.add((x,y))                            ###  (x,y) becomes a treated point
        nb=neighbours(x,y,dim[0]-1,dim[1]-1)         ###  computes list of neighbours of (x,y)
        for i in nb:
                start.discard(i)                    ###  removes i from start if i exists in start
                if i not in treat:                  ###  neighbor point is only interesting if it is not already treated
                        if math.isnan(vx[x,y]) or math.isnan(vx[i]) or math.isnan(vy[x,y]) or math.isnan(vy[i]):        ###  if any point is nan, only the future neighbor points are interesting, but i doesn't belong to the segment -> has to become a possible start point
                                start.add(i)
                        else:
                                if abs(gradients(x,y,i[0],i[1],vx,vy)[0])<abs(threshold(x,y,i[0],i[1],prior_vx,prior_vy,w,e_const)[0]) and (abs(gradients(x,y,i[0],i[1],vx,vy)[1])<abs(threshold(x,y,i[0],i[1],prior_vx,prior_vy,w,e_const)[1])):   ###  gradient constraint
                                        seg.append(i)                    ###  point has to be added to the actual segment 
                                        rekgrad(i[0],i[1],treat,seg,start,dim,vx,vy,prior_vx,prior_vy,w,e_const)     ###  same procedure for neighbour i
                                else:
                                        start.add(i)   ###  neighbor i doesn't belong to the actual segment
                                        
