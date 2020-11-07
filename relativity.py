import numpy as np 


def make4from3(vec):
    vec_4 = np.zeros(4)
    vec_4[0] = 0.0
    vec_4[1:] = vec
    return vec_4


def gamma(v):
    #v is a scalar here: 
    return 1./np.sqrt(1-np.dot(v,v))

def lorentz_onaxis(v,axis):
    v = v[axis-1]
    gam = gamma(v)
    lam = np.identity(4)
    lam[0,0] = gam 
    lam[0,axis] = -gam*v
    lam[axis,0] = -gam*v
    lam[axis,axis] = gam
    return lam


def lorentz(v):
    vsq = np.dot(v,v)
    vs = np.sqrt(vsq)
    gam = gamma(vs)


    boost = np.zeros((4,4))
    boost[0,0] = gam
    boost[0,1:] = -gam*v
    boost[1:,0] = -gam*v
    boost[1,1] = boost[2,2] = boost[3,3] = 1 
    boost[1:,1:] += (gam-1)*np.outer(v,v)/vsq

    return boost  