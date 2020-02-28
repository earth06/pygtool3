from numba import jit
import numpy as np
iso_p=np.array([1000,950,900,850,800,750,700,650,600,550,500,\
                         450,400,350,300,250,200,150,100,50,25,10,1])


@jit
def sig2isopiestic(data,p3d,convP,idim=128,jdim=64,kmax=36):
    iso_data=np.full((convP.size,jdim,idim),np.nan)
    for iy in range(jdim):
        for ix in range(idim):
            for ip,pz in enumerate(convP):
                for iz in range(kmax-1):
                    if (p3d[iz+1,iy,ix] <= pz <p3d[iz,iy,ix] ):
                        delp=p3d[iz,iy,ix]-p3d[iz+1,iy,ix]
                        fact= (pz-p3d[iz+1,iy,ix])/delp
                        iso_data[ip,iy,ix]=data[iz,iy,ix]*fact+data[iz+1,iy,ix]*(1.0-fact)
    return iso_data


def sig2isopiesticpy(data,p3d,convP=None,idim=128,jdim=64,kmax=36):
    """
    interpolate sigma scaled array into isopiestic array
    
    Parameters
    ----------
    data :numpy.ndarray (sigma,lat,lon)
         target data
    p3d  :numpy.ndarray (sigma,lat,lon) 
         pressure
    convP:array_like 
         new pressure scale
    
    Returns
    --------
    iso_data :numpy.ndarray
        array which converted to p-scale
    """

    if(type(convP) != np.ndarray):
        convP=np.array([1000,950,900,850,800,750,700,650,600,550,500,\
                         450,400,350,300,250,200,150,100,50,25,10,1])
    if(data.dtype != np.dtype('float64')):
        data=data.astype('float64')
    iso_data=sig2isopiestic(data,p3d,convP,idim=idim,jdim=jdim,kmax=kmax)
    return iso_data
