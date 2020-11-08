import numpy as np 
from intersection import intersect
import relativity as rel 
from plane import Plane 
from box import Box
import gif
@gif.frame
def boosted_reference(planeList):
    #initialization 
    Nplanes = len(planeList) 
    Nx, Ny = 3*192,3*108
    imagingX = 160
    imagingY = 90
    imagingPlane = 200
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
    for ind,pl in enumerate(planeList):
        tIntersects = intersect(pl,rays) 
        rInter =  rays*tIntersects[:,np.newaxis]
        # vel_4 * tInter[:,np.newaxis]
        intersectingRayIndices = rayInds[np.logical_and(np.logical_and(leastT > tIntersects, tIntersects>0), pl.inPlane(pl.toPrimedFrame(rInter)))]
        #np.arange(Nrays)[np.logical_and(leastT > tIntersects, tIntersects>np.zeros(Nrays))]
        intersectingPlaneIndex[intersectingRayIndices] = ind 
        leastT[intersectingRayIndices] = tIntersects[intersectingRayIndices]

    #compute the location of first intersection: 
    r1_4 = rays*tIntersects[:,np.newaxis] #np.multiply(np.tile(leastT,4).reshape((Nrays,4)),rays)
    #now, compute the color contributed by each plane at the point of intersection:
    numPlaneHits = np.array([np.sum((intersectingPlaneIndex == i)) for i in range(Nplanes)])
    raysIntersectingPlanes = [ rayInds[(intersectingPlaneIndex == i)] for i in range(Nplanes)]
    raysIntersectingSky = (rayInds[intersectingPlaneIndex == -1])
    print(raysIntersectingSky)
    rayRGB = np.zeros([Nrays,3],dtype = np.int32)
    for ind,pl in enumerate(planeList):
        intersectingRayInds = raysIntersectingPlanes[ind]
        #######################IntersectionRayInds has 0 size
        rayRGB[intersectingRayInds] = pl.boostedColor(rays[intersectingRayInds])
        # rayRGB[intersectingRayIndices,:] = color[intersectingRayIndices]
    # print(intersectingPlaneIndex)
    rayRGB[raysIntersectingSky] = np.array([0,25,50],dtype=np.int32)
    print('misses: ',np.size(raysIntersectingSky), 'of ', Nrays)
    #TODO: output the ray RGBs into an image
    screenRGB = np.reshape(rayRGB,[Nx,Ny,3])

    import matplotlib.pyplot as plt 
    plt.imshow(np.transpose(screenRGB,axes = (1,0,2)),origin = 'lower')

frames=[]
for angle in np.linspace(0,2,10):
    v = np.array([0.1,0.1,0.1])
    boost = rel.lorentz(v)
    #todo: plane class: 
    theta,phi = 0.,0.0
    colors = ([np.array([255,255,255])]*6)
    colors[0] = colors[1] = np.array([0,255,0])
    colors[2] = colors[3] = np.array([255,0,0])
    colors[4] = colors[5] = np.array([0,0,255])
    z = 300
    b = Box(boost,np.array([-z*v[0],-z*v[1],z]),np.array([50,50,50]),np.pi*np.array([angle,-0.0,0.]),colors = colors)
    planeList = b.planes
    frames.append(boosted_reference(planeList))
gif.save(frames,'test.gif',duration=10,unit='s',between='startend')

