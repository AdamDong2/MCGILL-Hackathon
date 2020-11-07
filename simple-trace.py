import numpy as np 


v = np.array([0.6,0,0])

#todo: compute Lambda 

planeList = []
#todo: plane class: 
#initialization 


Nx, Ny = 160,90
pixelX,pixelY = np.meshgrid(np.arange(0,))
Nrays = np.size(pixels) #can be more later if we want anti-aliasing
rays = np.zeros([Nrays,4])

for pl in planeList:
    tIntersects = intersection(pl,rays)