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
    Parameter
    -------------
    file  : string
         filename
    count : int, default 1
         total number of model data
    x,y,z : int, default (x,y,z)=(128,64,36)
        num of each coordinate.
    
    Return
    -------
    gtool3d :pygtool3.pygtool_core.Gtool3d
    """
    gtool3d=Gtool3d(file,count=count,x=x,y=y,z=z)
    return gtool3d
def read2d(file,count=1,x=128,y=64):
    """
    Parameter
    -------------
    file : string
        filename
    count : int, default 1
        total number of data
    x,y : int, default (x,y)=(128,64)
        num of each coordinate 
    
    Return
    -------
    gtool2d : pygtool3.pygtool_core.Gtool2d
    """
    gtool2d=Gtool2d(file,count=count,x=x,y=y)
    return gtool2d
def readgrid(x=128,y=64,lonfile=None,latfile=None):
    """
    Parameter
    -------------
    x,y : int, default (x,y)=(128,64)
        num of each coordinate
    lonfile,latfile : string, default None
        gtool3 coordinate file
        in default case this reads GTAXDIR/GTAXLOC.GLON(x),GTAXLOC.GGLA(y) 
        
    Return
    -------
    gtoolgrid : pygtool3.pygtool_core.GtoolGrid
    """
    gtoolgrid=GtoolGrid(x=x,y=y,lonfile=lonfile,latfile=latfile)
    return gtoolgrid
def readsigma(z=36,gtaxfile='GTAXLOC.HETA36'):
    """
    Parameter
    -------------
    z : int, default 36
        num of z coordinate
    gtaxfile : string, default:GTAXLOC.HETA36
        gtool3 coordinate file
    Return
    -------
    gtoolsigma : `pygtool3.pygtool_core.Gtoolsigma`
    """
    gtoolsigma=GtoolSigma(z=z,GTAXFILE=gtaxfile)
    return gtoolsigma
def readpressure(z=35,gtaxfile='GTAXLOC.AR5PL35'):
    """
    Parameter
    --------------
    z : int, num of z grid
    gtaxfile :string, default 'GTAXLOC.AR5PL35'
        coordinate file  
    Return
    ------------
    gtoolpres : pygtool3.pygtool_core.GtoolPressure
    """
    gtoolpres=GtoolPressure(z=z,GTAXFILE=gtaxfile)
    return gtoolpres
