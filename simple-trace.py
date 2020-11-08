import numpy as np 
from intersection import intersect


v = np.array([0.6,0,0])

#todo: compute Lambda 

planeList = []

Nplanes = len(planeList)
#todo: plane class: 
#initialization 
Nx, Ny = 160,90
imagingX = 
imagingPlane = 100
pixelX,pixelY = np.meshgrid(np.linspace(-imagingX,imagingX,Nx),np.linspace(-imagingY,imagingY,Ny))
Nrays = np.size(pixels) #can be more later if we want anti-aliasing
rays = np.zeros([Nx,Ny,4])
rays[:,:,0] = 1.0
rays[:,:,1] = pixelX
rays[:,:,2] = pixelY
rays[:,:,3] = imagingPlane
rays[:,:,1:] /= 


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
