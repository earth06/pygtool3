"""
`pygtool3.pygtool` is a interface to pygtool3.
It opens gtool3 formatted data which was developed by Numaguchi(1999)
We have to know whether input data is 2D or 3D in advance.
"""
import sys
import pathlib
thisdir=str(pathlib.Path(__file__).resolve().parent)
sys.path.append(thisdir)
from pygtool_core import Gtool3d,Gtool2d,GtoolGrid,GtoolSigma,GtoolPressure
import cartopy_toolkit as ckit
import gtplot
import gtutil
import gtcalic
def read3d(file,count=1,x=128,y=64,z=36):
    """
    read gtool 3D data

    Parameters
    -----------
    file  :string
         filename
    count :int, default 1
         total number of model data
    x,y,z :int, default (x,y,z)=(128,64,36)
        num of each coordinate.

    Returns
    -------
    gtool3d :pygtool3.pygtool_core.Gtool3d
        3D gtool formatted object
    """
    gtool3d=Gtool3d(file,count=count,x=x,y=y,z=z)
    return gtool3d
def read2d(file,count=1,x=128,y=64):
    """
    read gtool 2d data

    Parameters
    ----------
    file :string
        filename
    count :int, default 1
        total number of data
    x,y :int, default (x,y)=(128,64)
        num of each coordinate 

    Returns
    -------
    gtool2d :pygtool3.pygtool_core.Gtool2d
        2D gtool formatted object
    """
    gtool2d=Gtool2d(file,count=count,x=x,y=y)
    return gtool2d
def readgrid(x=128,y=64,lonfile=None,latfile=None):
    """
    read gtool horizontal coordinate

    Parameters
    ----------
    x,y :int, default (x,y)=(128,64)
        num of each coordinate
    lonfile,latfile :string, default None
        gtool3 coordinate file
        in default case this reads GTAXDIR/GTAXLOC.GLON(x),GTAXLOC.GGLA(y) 
    
    Returns
    -------
    gtoolgrid :pygtool3.pygtool_core.GtoolGrid
        gtool horizontal grid object
    """
    gtoolgrid=GtoolGrid(x=x,y=y,lonfile=lonfile,latfile=latfile)
    return gtoolgrid
def readsigma(z=36,gtaxfile='GTAXLOC.HETA36'):
    """
    read gtool sigma coordinate

    Parameters
    ----------
    z :int, default 36
        num of z coordinate
    gtaxfile :string, default:GTAXLOC.HETA36
        gtool3 coordinate file

    Returns
    -------
    gtoolsigma :pygtool3.pygtool_core.Gtoolsigma
        gtool3 sigma-vertical coordinate object
    """
    gtoolsigma=GtoolSigma(z=z,GTAXFILE=gtaxfile)
    return gtoolsigma
def readpressure(z=35,gtaxfile='GTAXLOC.AR5PL35'):
    """
    read gtool pressure coordinate

    Parameters
    ----------
    z :int, num of z grid
    gtaxfile :string, default 'GTAXLOC.AR5PL35'
        coordinate file

    Returns
    -------
    gtoolpres :pygtool3.pygtool_core.GtoolPressure
        gtool3 p-vertical coordinate object
    """
    gtoolpres=GtoolPressure(z=z,GTAXFILE=gtaxfile)
    return gtoolpres
