import numpy as np 
import healpy as hp 
import matplotlib.pyplot as plt 
import random

c=3e8 #m/s

def gamma(v):
    return 1/np.sqrt(1-v**2)

#def ChangeDir(n,v):

def ChangeDir3D(nvec,vvec):
    n_unit=nvec/np.sqrt(np.dot(nvec,nvec))
    v_unit=vvec/np.sqrt(np.dot(vvec,vvec))
    v_mag=np.sqrt(np.dot(vvec,vvec))
    nv_dot=np.dot(n_unit,v_unit)
    gam=gamma(v_mag)
    fac1=((gam-1)*nv_dot+gam*v_mag)/(gam*(1+v_mag*nv_dot))
    fac2=1/(gam*(1+v_mag*nv_dot))
    return fac1*v_unit+fac2*n_unit

def ChangeColor3D(nvec,nu,vvec):
    n_unit=nvec/np.sqrt(np.dot(nvec,nvec))
    v_unit=vvec/np.sqrt(np.dot(vvec,vvec))
    v_mag=np.sqrt(np.dot(vvec,vvec))
    gam=gamma(v_mag)
    nv_dot=np.dot(n_unit,v_unit)
    return nu/(gam*(1+v_mag*nv_dot))

def ChangeDir3D_prim(nvec,vvec):
    n_unit=nvec/np.sqrt(np.dot(nvec,nvec))
    v_unit=vvec/np.sqrt(np.dot(vvec,vvec))
    v_mag=np.sqrt(np.dot(vvec,vvec))
    nv_dot=np.dot(n_unit,v_unit)
    gam=gamma(v_mag)
    fac1=((gam-1)*nv_dot-gam*v_mag)/(gam*(1-v_mag*nv_dot))
    fac2=1/(gam*(1-v_mag*nv_dot))
    return fac1*v_unit+fac2*n_unit

def ChangeColor3D_prim(nvec,nu,vvec):
    n_unit=nvec/np.sqrt(np.dot(nvec,nvec))
    v_unit=vvec/np.sqrt(np.dot(vvec,vvec))
    v_mag=np.sqrt(np.dot(vvec,vvec))
    gam=gamma(v_mag)
    nv_dot=np.dot(n_unit,v_unit)
    return nu*(gam*(1+v_mag*nv_dot))

def add_polca(map,pix,nside,radius,val=100):
    n3d=hp.pix2vec(nside, pix)
    pixpolca=hp.query_disc(nside,n3d,radius)
    map[pixpolca]=val
    return



nside=128
nside2=64

radius=np.deg2rad(2)

#n3d=pix2vec(nside,ipix)
#pixpolca=hp.query_disc(nside,vec,radius (radians))

map_1=np.ones(hp.nside2npix(nside))
map_1_small=np.ones(hp.nside2npix(nside2))

for i in range(0,70):
    pix=random.randint(0,len(map_1)-1)
    add_polca(map_1,pix,nside,radius)

hp.mollview(map_1,cmap='bwr_r',min=0,max=2)
plt.show()

hp.mollview(hp.ud_grade(map_1,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

#hp.orthview(map_1)
#plt.show()

map_2=np.zeros_like(map_1)
map_3=np.zeros_like(map_1)
map_4=np.zeros_like(map_1)
map_5=np.zeros_like(map_1_small)
map_6=np.zeros_like(map_1_small)
vvec=np.ones(3)
vvec[0]=0.5
vvec[1]=0.5
vvec[2]=0.5
vmag=0.5 #units of c
vvec=0.5*vvec/np.sqrt(np.dot(vvec,vvec))
print(vvec)
print(np.sqrt(np.dot(vvec,vvec)))

# for j in range(0,len(map_1)):
#     #get the pixel of the old map, boost it to the new placement on the new map?
#     #change the color of the pixel due to the boost
#     nvec=hp.pix2vec(nside,j)
#     nvec_new=ChangeDir3D(nvec,vvec)
#     pix_new=hp.vec2pix(nside,nvec_new[0],nvec_new[1],nvec_new[2])
#     pix_new2=hp.vec2pix(nside2,nvec_new[0],nvec_new[1],nvec_new[2])
#     nu_val=map_1[j]
#     nu_new=ChangeColor3D(nvec,nu_val,vvec)
#     #print(nu_new)
#     map_2[j]=nu_new
#     map_3[pix_new]=map_1[j]
#     map_6[pix_new2]=map_1[j]
#     map_4[pix_new]=nu_new
#     map_5[pix_new2]=nu_new

for j in range(0,len(map_2)):
    nvec=hp.pix2vec(nside,j)
    nvec_new=ChangeDir3D_prim(nvec,vvec)
    pix_new=hp.vec2pix(nside,nvec_new[0],nvec_new[1],nvec_new[2])
    pix_new2=hp.vec2pix(nside2,nvec_new[0],nvec_new[1],nvec_new[2])
    nu_val=map_1[j]
    nu_new=ChangeColor3D_prim(nvec,nu_val,vvec)
    nu_val2=map_1[pix_new]
    nu_new2=ChangeColor3D_prim(nvec,nu_val2,vvec)
    #print(nu_new)
    map_2[j]=nu_new
    map_3[j]=map_1[pix_new]
    #map_6[pix_new2]=map_1[j]
    map_4[j]=nu_new2
    #map_5[pix_new2]=nu_new


hp.mollview(hp.ud_grade(map_2,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

hp.mollview(hp.ud_grade(map_3,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

hp.mollview(hp.ud_grade(map_4,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

#hp.mollview(hp.ud_grade(map_5,nside2),cmap='bwr',min=0,max=2)
#plt.show()

hp.orthview(hp.ud_grade(map_2,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

hp.orthview(hp.ud_grade(map_3,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

hp.orthview(hp.ud_grade(map_4,nside2),cmap='bwr_r',min=0,max=2)
plt.show()

#hp.orthview(map_2)#,cmap='Greys')
#plt.show()