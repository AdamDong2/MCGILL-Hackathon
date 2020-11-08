from plane import Plane 
import numpy as np 
from scipy.spatial.transform import Rotation
import relativity as rel 


class Box:
    def __init__(self,Lambda,r0,l123_prime,eulerAngles,colors=([np.array([255,255,255])]*6)):
        #make a fake plane at r0, to get access to the transformations 
        tPlane = Plane(Lambda,r0,np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]))
        rot = Rotation.from_euler('xyz',eulerAngles)

        # l123_prime is the xwid/2, ywid/2, zwid/2, before rotation.
        # euler angles is a tuple or a array(3) of rotation angles. 
        # r0 is the center. 

        lps = np.zeros(shape=(3,3))
        lps[0,:] = np.array([l123_prime[0],0,0])
        lps[1,:] = np.array([0,l123_prime[1],0])
        lps[2,:] = np.array([0,0,l123_prime[2]])

        #APPLYING THE ROTATION:
        lps_rot = rot.apply(lps)

        self.planes = []

        #theoretically working
        # def addPlane(planeind,offset_ind,l1pind,l2pind):
        #     offset_p = lps_rot[offset_ind]
        #     offset = tPlane.fromPrimedFrame(rel.make4from3(offset_p))
        #     print(offset,offset[1:]-r0,tPlane.toPrimedFrame(offset))
        #     offset[1:]-=r0
        #     offset_sign = (1 -  2*(planeind%2))
        #     plane_r0 = r0 + offset[1:]*offset_sign
            
        #     print(planeind,r0,offset[1:]*offset_sign)

        #     l1p = lps_rot[l1pind]
        #     l2p = lps_rot[l2pind]
        #     nhat_p = offset_sign*offset_sign * offset_p / np.sqrt(np.dot(offset_p,offset_p))

        #     pl = Plane(Lambda,plane_r0,nhat_p,l1p,l2p,colors[planeind])
        #     self.planes.append(pl)

            
        #borked, but kinda works? 
        def addPlane(planeind,offset_ind,l1pind,l2pind):
            offset_p = lps_rot[offset_ind]
            offset = np.dot(tPlane.Lambda_inv,rel.make4from3(offset_p))# tPlane.fromPrimedFrame(rel.make4from3(offset_p))
            #fix the time part, because we don't know which t' should have been used in the prime frame. Basically, t' = 0 only at the origin of the plane, not the edges...
            tprime = offset[0] / Lambda[0,0]
            tcontrib = np.dot(tPlane.Lambda_inv,np.array([tprime,0,0,0]))
            offset -= tcontrib
            
            
            print(offset,offset[1:]-r0,tPlane.toPrimedFrame(offset))
            # offset[1:]-=r0
            offset_sign = (1 -  2*(planeind%2))
            plane_r0 = r0 + offset[1:]*offset_sign
            
            print(planeind,r0,offset[1:]*offset_sign)

            l1p = lps_rot[l1pind]
            l2p = lps_rot[l2pind]
            nhat_p = offset_sign*offset_sign * offset_p / np.sqrt(np.dot(offset_p,offset_p))

            pl = Plane(Lambda,plane_r0,nhat_p,l1p,l2p,colors[planeind])
            self.planes.append(pl)

        addPlane(0,0,1,2)
        addPlane(1,0,1,2)
        addPlane(2,1,2,0)
        addPlane(3,1,2,0)
        addPlane(4,2,0,1)
        addPlane(5,2,0,1)
    
