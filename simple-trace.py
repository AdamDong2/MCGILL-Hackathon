import numpy as np 
from intersection import intersect
import relativity as rel 
from plane import Plane 

v = np.array([0.0,0,0])
boost = rel.lorentz(v)

#todo: plane class: 
theta,phi = 0.,0.0
plane1 = Plane(boost,np.array([0,0,500]),np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)]),np.array([20,0.0,0.0]),np.array([20,0.0,0.0]) )

planeList = [plane1]
Nplanes = len(planeList)

#initialization 
Nx, Ny = 190,120
imagingX = 160
imagingY = 90
imagingPlane = 100
pixelX,pixelY = np.meshgrid(np.linspace(-imagingX,imagingX,Nx),np.linspace(-imagingY,imagingY,Ny),indexing = 'ij')
Nrays = Nx*Ny #can be more later if we want anti-aliasing
rays = np.zeros([Nx,Ny,4])
rays[:,:,0] = 1.0
rays[:,:,1] = pixelX
rays[:,:,2] = pixelY
rays[:,:,3] = imagingPlane
#forbidden loop -- if you have a nicer way to write this, let me know.
for i in range(Nx):
    for j in range(Ny):
        ray = rays[i,j,:]
        rays[i,j,1:] /= np.sqrt(np.dot(ray,ray))
#shaping the rays 
rays = np.reshape(rays,[Nx*Ny,4])
#to obtain the original configuration, use: rays = np.reshape(rays,[Nx,Ny,4])



#compute which plane is first intersected by each ray: 
rayInds = np.arange(Nrays)
intersectingPlaneIndex = -1*np.ones(Nrays,dtype=np.int32)
leastT = 1e99 * np.ones(Nrays)
print(leastT)
for ind,pl in enumerate(planeList):
    tIntersects = intersect(pl,rays) 
    print(tIntersects.shape)
    intersectingRayIndices = rayInds[np.logical_and(leastT > tIntersects, tIntersects>0)]
    #np.arange(Nrays)[np.logical_and(leastT > tIntersects, tIntersects>np.zeros(Nrays))]
    intersectingPlaneIndex[intersectingRayIndices] = ind 
    leastT[intersectingRayIndices] = tIntersects[intersectingRayIndices]

#compute the location of first intersection: 
r1_4 = np.multiply(np.tile(leastT,4).reshape((Nrays,4)),rays)
#now, compute the color contributed by each plane at the point of intersection:
numPlaneHits = np.array([np.sum((intersectingPlaneIndex == i)) for i in range(Nplanes)])
raysIntersectingPlanes = [ rayInds[(intersectingPlaneIndex == i)] for i in range(Nplanes)]

rayRGB = np.zeros([Nrays,3],dtype = np.int32)
for ind,pl in enumerate(planeList):
    intersectingRayInds = raysIntersectingPlanes[ind]
    rayRGB[intersectingRayInds] = pl.boostedColor(rays[intersectingRayInds],r1_4[intersectingRayInds], np.array([500,0,-500,0]),100.0)
    # rayRGB[intersectingRayIndices,:] = color[intersectingRayIndices]





#TODO: output the ray RGBs into an image
screenRGB = np.reshape(rayRGB,[Nx,Ny,3])

import matplotlib.pyplot as plt 
plt.imshow(screenRGB,'lower')
plt.show()