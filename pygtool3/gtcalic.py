import numpy as np
import pandas as pd
import pathlib
import sys
thisdir=str(pathlib.Path(__file__).resolve().parent) 
sys.path.append(thisdir)
from pygtool_core import Gtool3d,Gtool2d,GtoolGrid,GtoolSigma
mid_lon=np.arange(1.40625,360.1,2.8125)
#def lonlabel(left=):
#def latlabel(left=-90,right=90,dlat=30):
#    latlist=[]
#    for i in range(lfet,right,dlat)

def weighted_mean(arr,area):
    """
    Parameter
    --------------
    arr   :array_like
    area  :array_like
    Return
    --------------
    weighted_mean :np.ndarray
    """
    
    weighted_mean=(arr*area).sum()/area.sum()
    return weighted_mean

def get_area(dlon=2.5e0,dlat=2.5e0):
    """
    """
    er=6370e3
    xxtmp,yytmp=np.meshgrid(np.arange(0,360,dlon),np.arange(90,-90.1,-dlat))
    area=(er**2)*(np.deg2rad(dlon)*(np.sin(np.deg2rad(yytmp[0:-1,:]))\
                                  -np.sin(np.deg2rad(yytmp[1:,:])))\
)
    return area
def corre_coef(x,y):
    """
    args  type
    -------------------------
    x     np.ndarray((time,y,x))
    y     np.ndarray((time,y,x))
    
    return  type
    -------------------------
    correlation  np.ndarray((y,x))
    """
    xmean=x.mean(axis=0)
    ymean=y.mean(axis=0)
    xyarr=x*y
    xymean=xyarr.mean(axis=0)
    x2mean=(x**2).mean(axis=0)
    y2mean=(y**2).mean(axis=0)
    xystd=xymean-(x.mean(axis=0)*y.mean(axis=0))
    correlation=(xymean-xmean*ymean)/np.sqrt((x2mean-xmean**2)*(y2mean-ymean**2))
    return correlation

def zscore(x,axis=None,ddof=0):
    """ 
    return zscore standalization
           x =(x - x.mean)/x.std
    average=0 std=1

    Parameters
    -------------------
    x : numpy.ndarray(x,y)
    axis :int 0 #caliculate each col
              1 #           each row
    ddof :int 0 #when caliculate std, devide by n
              1 #                   , devide by n-1
    Returns
    --------------------
    zcore : np.ndarray(x,y)
    """
    xmean=x.mean(axis=axis,keepdims=True)
    xstd=np.std(x,axis=axis,keepdims=True,ddof=ddof)
    zscore  =(x-xmean)/xstd
    return zscore

def min_max(x,axis=None):
    """
    return min_max standalization
           x = (x-x.min)/(x.max-x.min)
    min=0 max=1

    Parameters
    -------------------
    x : numpy.ndarray(x,y)
    axis :int 0 #caliculate each col
              1 #           each row

    Returns
    --------------------
    result : np.ndarray(x,y)
    """
    xmin =x.min(axis=axis,keepdims=True)
    xmax =x.max(axis=axis,keepdims=True)
    result = (x-xmin)/(xmax-xmin)
    return result
def normdate_to_datetime():
    """
    converting floating date into datetimeindex
    """
    
    return
def getcmass_column(cmass=None,ps=None,T=None,sigma=None,sigma_M=None,\
                    timestep=0,zmax=None,fact=1.0e0,cyclic=False):
    """
    conduct vertical integration and return column concentration

    Parameter
    ---------
    Cmass : Gtool3d or numpy.ndarray, mass concentration
    ps : Gtool2d or numpy.ndarray, surface pressure[hPa]
    T : Gtool3d or numpy.ndarray , temperature[K]
    sigma : GtoolSigma,sigmascale for middle grid
    sigma_M : GtoolSigma,sigmascale for boudary grid
    timestep : int, set model timestep if passed data is Gtool* instance
    cyclic : bool, whether longitude is cyclic or not.
    fact :float, factor for adjusting unit of column concentration
 
    Return
    ----------
    column : numpy.ndarray, column concentration of passed tracer
    """
    P=(sigma.get_pressure(ps,timestep=timestep,cyclic=cyclic))*1e2
    PM=(sigma_M.get_pressure(ps,timestep=timestep,cyclic=cyclic))*1e2
    dp=PM[1:,:,:]-PM[:-1,:,:]
    grav=9.8e0
    if isinstance(T,Gtool3d):
        rho=(P/287.0/T.getarr(timestep=timestep,cyclic=cyclic))
    else:
        rho=(P/287.0/T)
    dz=-dp/(rho*grav)
    if isinstance(cmass,Gtool3d):
        col3D=cmass.getarr(timestep=timestep,cyclic=cyclic)*dz
    else:
        col3D=cmass*dz
    if zmax is None:
        column=col3D[0:,:,:].sum(axis=0)*fact
    else:
        column=col3D[0:zmax,:,:].sum(axis=0)*fact
    return column
