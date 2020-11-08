import numpy as np 
from relativity import *
from scipy.constants import h, c, k

from colours import cs_hdtv
cs = cs_hdtv

def planck(lam, T):
    """ Returns the spectral radiance of a black body at temperature T.

    Returns the spectral radiance, B(lam, T), in W.sr-1.m-2 of a black body
    at temperature T (in K) at a wavelength lam (in nm), using Planck's law.

    """
    
    lam_m = lam / 1.e9
    #print(np.size(lam))
    #print(np.size(T))
    fac = h*c/lam_m/k/T
    B = 2*h*c**2/lam_m**5 / (np.exp(fac) - 1)
    return B

class Plane:
    def __init__(self,Lambda,r0,nhat_prime,l1_prime,l2_prime,plane_colour=np.array([255,255,255]),temperature=6500):
        #Lambda is the lorentz boost from the observer frame to the plane frame 
        #r0 is the plane's position at t = 0 in the observer frame
        #nhat is the plane orientation in the plane frame
        #l1 and l2 are orthogonal vectors from the center to their respective edges. 

        #we should compute nhat
        self.r0 = r0 
        self.r0_4 = make4from3(r0)
        self.Lambda = Lambda 
        self.Lambda_inv = np.linalg.inv(Lambda)

        self.nhat_prime = nhat_prime
        nhat_prime_4 = make4from3(nhat_prime)
        self.nhat_prime_4 = nhat_prime_4
        self.nhat = np.dot(Lambda,nhat_prime_4)
        self.a = -np.dot(Lambda,make4from3(r0))

        self.l1_prime = l1_prime
        self.l1sq = np.dot(l1_prime,l1_prime)
        self.l2_prime = l2_prime 
        self.l2sq = np.dot(l2_prime,l2_prime)
        self.temperature =temperature
        self.plane_colour = np.array(plane_colour) 
    def inPlane(self,r_prime):
        #given the r_prime, Nx4 coordinates of the intersections with the infinite plane, return whether we are in the plane
        if(r_prime.shape[1] == 4):
            d1,d2 = np.dot(r_prime[:,1:],self.l1_prime),np.dot(r_prime[:,1:],self.l2_prime)
        elif(r_prime.shape[1] == 3):
            d1,d2 = np.dot(r_prime,self.l1_prime),np.dot(r_prime,self.l2_prime)
        else:
            raise ValueError
        return np.logical_and(np.abs(d1)<self.l1sq,np.abs(d2)<self.l2sq)

    def toPrimedFrame(self,r):
        #computes the r_prime coordinates, given the 4-vectors in r: 
        rp = np.dot(self.Lambda,r.transpose()).transpose() 
        rp+=self.a
        return rp # np.dot(self.Lambda,r) + self.a

    def fromPrimedFrame(self,r_prime):
        #computes the r coordinates, given a 4-vector in the primed coordinate system:
        #from plane frame to observer frame
        return np.dot(self.Lambda_inv,r_prime - self.a)

    def boostedColor(self,rays):
        # assume collimated, single frequency light. Photons have source_momentum and occur in an intensity set by ``source_intensity''
        # returns an RGB?
        #rays -  n by 4 numpy array, is the 4-velocity of light ray hitting the plane from obs, norm to speed of 1
        #r_inters -- n by 4, 4 poisition of the intersection between the ray and the plane, a point in 4 space in obs ref frame
        #souce_momentum --
        # returns an RGB?
        print('original temperature')
        print('boosted temperature')
        boosted_temperature= self.boostedColor_raelyn(rays)*self.temperature
        print(boosted_temperature)
        lam = np.arange(380., 781., 5)
        my_rgbs=[]
        for temperature in boosted_temperature:
            spec = planck(lam, temperature)
            my_rgbs.append(255*cs.spec_to_rgb(spec))


        return my_rgbs
        

    def boostedColor_raelyn(self,rays):
        gamma=self.Lambda[0,0]
        vvec=self.Lambda[0,1:]/gamma
        vmag=np.sqrt(np.dot(vvec,vvec))
        vhat=vvec/vmag
        nvec=rays[:,1:]
        #return 1/(gamma*(1-vmag*np.dot(nvec,vhat)))
        return gamma*(1+vmag*np.dot(nvec,vhat))

