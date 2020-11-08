import numpy as np

from plane import Plane

def intersect(pl,rays):
    #rays is a n x 4 matrix
    #lets calculate the parameter t
    numerator=np.dot(pl.r0_4,pl.nhat)

    denominator = np.matmul(rays,pl.nhat)
    index=(denominator==0)
    t=np.zeros(len(denominator))
    t[~index]= np.divide(numerator[~index]/denominator[~index])
    t[index]=np.inf
    #t is a n dimensional array
    return t
