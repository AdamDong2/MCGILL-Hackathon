import numpy as np 
from relativity import *

class Plane: 
    def __init__(self,Lambda,r0,nhat_prime,l1_prime,l2_prime,plane_colour=np.array([255,255,255])):
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
        self.plane_colour = np.array(plane_colour) 
    def inPlane(self,r_prime):
        #given the r_prime, Nx4 coordinates of the intersections with the infinite plane, return whether we are in the plane
        if(r_prime.shape[1] == 4):
            return np.logical_and(np.dot(r_prime[:,1:],self.l1_prime) < self.l1sq,np.dot(r_prime[:,1:],self.l2_prime) < self.l2sq)
        elif(r_prime.shape[1] == 3):
            return np.logical_and(np.abs(np.dot(r_prime,self.l1_prime)) < self.l1sq, np.abs(np.dot(r_prime,self.l2_prime)) < self.l2sq)
        else:
            raise ValueError

    def toPrimedFrame(self,r):
        #computes the r_prime coordinates, given the 4-vectors in r: 
        rp = np.dot(self.Lambda,r.transpose()).transpose() 
        rp+=self.a
        return rp # np.dot(self.Lambda,r) + self.a

    def fromPrimedFrame(self,r_prime):
        #computes the r coordinates, given a 4-vector in the primed coordinate system: 
        return np.dot(self.Lambda_inv,r_prime - self.a)

    def boostedColor(self,rays,r_inters,source_momentum,source_intensity):
        # assume collimated, single frequency light. Photons have source_momentum and occur in an intensity set by ``source_intensity''
        # returns an RGB? 
        return self.plane_colour
