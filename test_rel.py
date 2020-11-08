import relativity as rel 
import numpy as np 

v = np.array([0.3,0.5,0])
lam  =(rel.lorentz(v))
laminv = rel.lorentz(-v)
laminv2 = np.linalg.inv(lam)
print(lam)
print(laminv)
print(laminv2)