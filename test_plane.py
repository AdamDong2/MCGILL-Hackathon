import numpy as np 
import matplotlib.pyplot as plt 
from plane import Plane 
xs,ys = np.arange(-190,190),np.arange(-100,100)
xx,yy = np.meshgrid(xs,ys,indexing ='ij')

theta = 0.15
pl = Plane(np.identity(4),np.zeros(3),np.array([0,0,1.]), 10*np.array([np.cos(theta),np.sin(theta),0]),20*np.array([-np.sin(theta),np.cos(theta),0]))
rs = np.zeros(shape = tuple(list(np.shape(xx)) + [3]))
rs[:,:,0] = xx
rs[:,:,1] = yy 
rs[:,:,2] = 0.0
rdest = np.reshape(rs,[rs.shape[0]*rs.shape[1],3],'F')
hits = pl.inPlane(rdest)
hits = np.reshape(hits,xx.shape,'F')

plt.imshow(hits)
plt.show()