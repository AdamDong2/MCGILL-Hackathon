import numpy as np

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
for i in range(Nx):
    for j in range(Ny):
        ray = rays[i,j,:]
        rays[i,j,1:] /= np.sqrt(np.dot(ray,ray))

rays_original = rays
rays = np.reshape(rays,[Nx*Ny,4])
rays_back = np.reshape(rays,[Nx,Ny,4])

print('reshaping back and forth errors: ',np.sum(rays_back!=rays_original))