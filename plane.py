import numpy as np 
import * from relativity

class Plane: 
    def __init__(Lambda,r0,nhat_prime,l1_prime,l2_prime):
        #Lambda is the lorentz boost from the observer frame to the plane frame 
        #r0 is the plane's position at t = 0 in the observer frame
        #nhat is the plane orientation in the plane frame
        #l1 and l2 are orthogonal vectors from the center to their respective edges. 

        #we should compute nhat
        self.r0 = r0 
        self.r0_4 = make4from3(r0)
        self.Lambda = Lambda 

        self.nhat_prime = nhat_prime
        nhat_prime_4 = make4from3(nhat_prime)
        self.nhat_prime_4 = nhat_prime_4
        self.nhat = np.dot(Lambda,nhat_prime_4)
        self.a = -np.dot(Lambda,make4from3(r0))

        self.l1_prime = l1_prime
        self.l1sq = np.dot(l1_prime,l1_prime)
        self.l2_prime = l2_prime 
        self.l2sq = np.dot(l2_prime,l2_prime)

    def inPlane(self,r_prime):
        #given the r_prime coordinates of the intersections with the infinite plane, return whether we are in the plane
        return np.logical_and(np.dot(r_prime,l1_prime) < l1sq,np.dot(r_prime,l2_prime) < l2sq)