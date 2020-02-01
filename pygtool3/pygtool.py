"""
`pygtool3.pygtool` is a interface to pygtool3.
It opens gtool3 formatted data which was developed by Numaguchi(1999)
We have to know whether input data is 2D or 3D in advance.
"""
import sys
import pathlib
thisdir=str(pathlib.Path(__file__).resolve().parent)
sys.path.append(thisdir)
from pygtool_core import Gtool3d,Gtool2d,GtoolGrid,GtoolSigma
import cartopy_toolkit as ckit
import gtplot
import gtutil
import gtcalic
def read3d(file,count=1,x=128,y=64,z=36):
    """
    Parameter
    -------------
    file  : string, filename
    count : int, num of data, default:1
    x,y,z : int, num of each grid. default (x,y,z)=(128,64,36)
    
    Return
    -------
    gtool3d : `pygtool3.pygtool_core.Gtool3d`
    """
    gtool3d=Gtool3d(file,count=count,x=x,y=y,z=z)
    return gtool3d
def read2d(file,count=1,x=128,y=64):
    """
    Parameter
    -------------
    file : string, filename
    count : int, num of data, default:1
    x,y : int, num of each grid. default (x,y)=(128,64)
    
    Return
    -------
    gtool2d : `pygtool3.pygtool_core.Gtool2d`
    """
    gtool2d=Gtool2d(file,count=count,x=x,y=y)
    return gtool2d
def readgrid(x=128,y=64,lonfile=None,latfile=None):
    """
    Parameter
    -------------
    x,y : int, num of each grid. default (x,y)=(128,64)
    lonfile,latfile : string, gtool3 axis files
        default:None it reads GTAXDIR/GTAXLOC.GLON(x),GTAXLOC.GGLA(y) 
    Return
    -------
    gtoolgrid : `pygtool3.pygtool_core.GtoolGrid`
    """
    gtoolgrid=GtoolGrid(x=x,y=y,lonfile=lonfile,latfile=latfile)
    return gtoolgrid
def readsigma(z=36,gtaxfile='GTAXLOC.HETA36'):
    """
    Parameter
    -------------
    z : int, num of z grid
    gtaxfile : string, default:GTAXLOC.HETA36

    Return
    -------
    gtoolsigma : `pygtool3.pygtool_core.Gtoolsigma`
    """
    gtoolsigma=GtoolSigma(z=z,GTAXFILE=gtaxfile)
    return gtoolsigma

