import numpy as np

from plane import Plane 

def intersect(pl,rays):
    #rays is a n x 4 matrix
    #lets calculate the parameter t
    numerator=np.dot(pl.r0_4,pl.nhat)
    denominator = np.matmul(rays,np.array(pl.nhat))
    index=(denominator==0)
    print(~index)
    t=np.zeros(len(denominator))
    t[~index]= np.divide(numerator,denominator[~index])
    t[index]=np.inf
    #t is a n dimensional array
    return t

if __name__=="__main__":
    test_rays = np.tile(np.array([1,2,3,4]),100)
    test_rays=test_rays.reshape((100,4))
    theta=0.15
    pl = Plane(np.identity(4),np.zeros(3),np.array([0,0,1.]), 10*np.array([np.cos(theta),np.sin(theta),0]),20*np.array([-np.sin(theta),np.cos(theta),0]))
    intersect(pl,test_rays)    


