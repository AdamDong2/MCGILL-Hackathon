import numpy as np 
from intersection import intersect


v = np.array([0.6,0,0])

#todo: compute Lambda 

planeList = []

Nplanes = len(planeList)
#todo: plane class: 
#initialization 
Nx, Ny = 190,120
imagingX = 160
imagingY = 90
imagingPlane = 100
pixelX,pixelY = np.meshgrid(np.linspace(-imagingX,imagingX,Nx),np.linspace(-imagingY,imagingY,Ny),indexing = 'ij')
Nrays = np.size(Nx*Ny) #can be more later if we want anti-aliasing
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



intersectingPlaneIndex = -1*np.ones(Nrays,dtype=np.int32)
leastT = 1e99 * np.ones(Nrays)
rayRGB = np.zeros([Nrays,3],dtype = int32)
for ind,pl in enumerate(planeList):
    color,tIntersects = intersect(pl,rays) 
    
    
    intersectingRayIndices = np.arange(Nrays)[np.logical_and(leastT > tIntersects, tIntersects>0)]
    intersectingPlaneIndex[intersectingRayIndices] = ind 
    leastT[intersectingRayIndices] = tIntersects[intersectingRayIndices]
    rayRGB[intersectingRayIndices,:] = color[intersectingRayIndices]

#TODO: output the ray RGBs into an image.
