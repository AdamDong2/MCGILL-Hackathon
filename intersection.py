import numpy as np

from plane import plane 

def intersect(pl,rays):
    #rays is a n x 4 matrix
    #lets calculate the parameter t
    numerator=np.dot(pl.r0_4,pl.nhat)

    denominator = np.matmul(rays,pl.nhat)
    if denominator!=0:
        t= np.divide(numerator/denominator)
    else:
        t=np.inf()
    #t is a n dimensional array
    return t
