import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
import matplotlib.colors as mcolors
import pandas as pd 
import numpy as np
import cartopy.crs as ccrs
import sys
import pathlib
thisdir=str(pathlib.Path(__file__).resolve().parent)
sys.path.append(thisdir)   
import cartopy_toolkit as ckit
from pygtool_core import Gtool3d,Gtool2d,GtoolGrid,GtoolSigma,isgtoolinstance

sformat=ticker.ScalarFormatter(useMathText=True)

@ticker.FuncFormatter
def latformatter(y,pos):
    if y== 0:
        NS='°'
    elif y <0:
        NS='°S'
    else:
        NS='°N'
    return '{:.0f}{}'.format(np.abs(y),NS)
@ticker.FuncFormatter
def lonformatter(x,pos):
    if x in [0,180,360] :
        EW='°'
    elif (0 < x < 180):
        EW='°E'
    else:
        x=360-x
        EW='°W'
    return '{:.0f}{}'.format(x,EW)
def set_lonticks(ax,dlon=30,labelsize=16):
    """
    set xticks as logitude
    
    Parameter
    ----------
    ax  :matplotlib.axes
    dlon:float, default 30
        logitude interval
    labelsize:int, default 16
        tick label size
    Return
    ----------
    ax
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(dlon))
    ax.xaxis.set_major_formatter(lonformatter)
    ax.xaxis.set_tick_params(labelsize=labelsize)
    return ax
def set_latticks(ax,dlat=15,labelsize=16):
    """
    set xticks as latitude
    
    Parameter
    ----------
    ax  :matplotlib.axes
    dlat:float, default 15
        logitude interval
    labelsize:int, default 16
        tick label size
    Return
    ----------
    ax
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(dlat))
    ax.xaxis.set_major_formatter(latformatter)
    ax.xaxis.set_tick_params(labelsize=labelsize)
    return ax
def YYlabel(ax,base=1,month=12,day=1,labelsize=14):
    ax.xaxis.set_major_locator(mdates.YearLocator(base=1,month=month,day=day))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    return ax 

def MMlabel(ax,labelsize=18):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \n %Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(labelsize=labelsize)
    return ax

def DDlabel(ax,labelsize=18):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \n %Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(labelsize=labelsize)
    return ax

def contourf(xx,yy,arr,cnum=20,clabelsize=14,extend='both',levels=None,\
    cmap='viridis',alpha=1,\
    na_values=-999,replace_nan=False,
    timestep=0,zsel=0,cyclic=False):
    """
    Parameter
    ---------------
    xx,yy  :numpy.ndarray
    arr    :numpy.ndarray or Gtool*D
    cnum    :int or float, default 20
            the number of contour
    cmap    :string, default 'viridis'
        colormap name
    extend :string, default 'both'
             whether fill contour when out of rang {both,neither,max,min}
    levels :array_like, default None
        set contour level manually
    alpha  :float, default 1
    timestep:int, default 0
        model timestep
    zsel :int, default 0
         select model layer for plot
    cyclic :bool, default False
        cyclic logntiude or not
    Return
    ----------------
    fig :matplotlib.Figure
    ax :matplotlib.Axes
    cbar :matplotlib.colorbar

    """
    sformat.set_powerlimits((-1,3))
    fig=plt.figure(figsize=(10,6),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    dat=isgtoolinstance(arr,timestep=timestep,cyclic=cyclic,zsel=zsel,replace_nan=replace_nan,
            na_values=na_values)
    if levels is None:
        delta=(np.nanmax(dat)-np.nanmin(dat))/(cnum)
        levels=np.arange(np.nanmin(dat),abs(np.nanmax(dat))*2 +delta,delta)[0:int(cnum)+1]
    cf=ax.contourf(xx,yy,dat
        ,levels=levels
        ,extend=extend
        ,cmap=cmap
        ,alpha=alpha
        ,transform=ccrs.PlateCarree())
    cbar=fig.colorbar(cf,cax
#        ,ticks=interval[::2]
        ,format=sformat
        ,orientation='horizontal')

    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(14)
    return fig,ax,cbar
def logcontourf(xx,yy,arr,subs=(1.0,),clabelsize=14,\
    vmin=None,vmax=None,\
    cmap='viridis',alpha=1,extend='both',offsetTextsize=14,\
    na_values=-999,replace_nan=False,
    timestep=0,cyclic=False,zsel=0):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :Gtool2d or Gtool3d or numpy.ndarray
        model data
    subs   :sequence of float, 'all','auto',None
           default=(1,) ex) (1.0,2.0) 
    cmap   :string, default 'viridis'
        colormap
    vmin   :float
        minimum value,default=arr.min()
    vmax   :float
        maximum value,default=arr.max()
    alpha  :float, default 1
    extend :string
        {'max','min','both','neither'}
    timestep:int, default 0
    zsel : int, default 0
    cyclic:bool, default False

    Return
    ----------------
    fig :matplotlib.Figure
    ax  :matplotlib.axes
    cbar:matplotlib.colorbar
    """
    fig=plt.figure(figsize=(10,6),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    dat=isgtoolinstance(arr,timestep=timestep,cyclic=cyclic,zsel=zsel,na_values=na_values,replace_nan=replace_nan)
    if vmin is None:
        vmin=np.nanmin(dat)
    if vmax is None:
        vmax=np.nanmax(dat)

    cf=ax.contourf(xx,yy,dat,
        vmin=vmin,vmax=vmax,
        cmap=cmap,
        extend=extend,
        alpha=alpha,
        locator=ticker.LogLocator(subs=subs),
        transform=ccrs.PlateCarree())
    cbar=fig.colorbar(cf,cax,
        extend=extend,
        ticks=ticker.LogLocator(subs=(1.0,)),
        format=ticker.LogFormatterSciNotation(),
        orientation='horizontal')
    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(offsetTextsize)
    return fig,ax,cbar
def pcolormesh(xx,yy,arr,subs=(1.0,),clabelsize=14,\
    vmin=None,vmax=None,scale='normal',\
    cmap='viridis',alpha=1,extend='both',offsetTextsize=14,\
    na_values=-999,replace_nan=False,
    timestep=0,cyclic=False,zsel=0):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :Gtool2d or Gtool3d or numpy.ndarray
        model data
    subs   :{sequence of float, 'all','auto',None}
           default=(1,) ex) (1.0,2.0) 
    cmap   :string
         colormap
    vmin   :float
        minimum value,default arr.min()
    vmax   :float
        maximum value,default arr.max()
    alpha  :float, default 1
    extend :string
        {'max','min','both','neither'}
    scale  :string
        {'normal','log'}
    Return
    ----------------
    fig :matplotlib.Figure
    ax  :matplotlib.Axes
    cbar:matplotlib.Colorbar
    """
    
    fig=plt.figure(figsize=(10,6),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    dat=isgtoolinstance(arr,timestep=timestep,cyclic=cyclic,zsel=zsel,replace_nan=replace_nan,na_values=na_values)
    if vmin is None:
        vmin=np.nanmin(dat)
    if vmax is None:
        vmax=np.nanmax(dat)
    norm={'normal':None,'log':LogNorm(vmin=vmin,vmax=vmax)}
    cf=ax.pcolormesh(xx,yy,dat,
        cmap=cmap,
        alpha=alpha,
        norm=norm[scale],
        transform=ccrs.PlateCarree())
    if scale=='log':
        cbar=fig.colorbar(cf,cax,
            extend=extend,
            ticks=ticker.LogLocator(subs=subs),
            format=ticker.LogFormatterSciNotation(),
            orientation='horizontal')
    else:
        cbar=fig.colorbar(cf,cax,extend=extend,orientation='horizontal')
    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(offsetTextsize)
    return fig,ax,cbar
def zonal_contourf(yy,zz,arr,cnum=20,clabelsize=14,extend='both',levels=None,\
            cmap='viridis',powerlimits=(-1,3),alpha=1,\
            dlat=15.0,labelsize=14,
            na_values=-999,replace_nan=False,
            ylabel='eta',
            timestep=0,xsel='mean',cyclic=False):
    """
    Parameter
    ---------------
    yy,zz  :array_like
    xsel   :int or string,{index of logitude,'mean'} 
    arr    :array_like
            input data
    cnum    :int or float
            the number of contour
    powerlimits:tuple
           exponent range
    
    
    Return
    ----------------
    fig
    ax
    cbar

    """
    sformat.set_powerlimits((powerlimits))
    fig=plt.figure(figsize=(9,6),facecolor='w')
    ax=fig.add_subplot(1,1,1)
    cax=fig.add_axes([0.25,0,0.5,0.05])
    if isinstance(arr,Gtool3d):
        dat=arr.getarr(cyclic=cyclic,timestep=timestep,replace_nan=replace_nan,na_values=na_values)[:,:,:]
    else:
        dat=arr[:,:,:]
    if xsel=='mean':
        dat=np.nanmean(dat[:,:,:],axis=2)
    else:
        dat=dat[:,:,xsel]
    set_latticks(ax=ax,dlat=dlat,labelsize=labelsize)
    if levels is None:
        delta=(np.nanmax(dat)-np.nanmin(dat))/(cnum)
        levels=np.arange(np.nanmin(dat),abs(np.nanmax(dat))*2 +delta,delta)[0:int(cnum)+1]

    cf=ax.contourf(yy,zz,dat
        ,levels=levels
        ,extend=extend
        ,cmap=cmap
        ,alpha=alpha)
    cbar=fig.colorbar(cf,cax
#        ,ticks=interval[::2]
        ,format=sformat
        ,orientation='horizontal')

    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(14)
#    ax.set_ylim(1,0)
    ax.grid()
    return fig,ax,cbar
def zonal_logcontourf(yy,zz,arr,cnum=20,clabelsize=14,extend='both',vmax=None,vmin=None,\
            cmap='viridis',powerlimits=(-1,3),alpha=1,\
            dlat=15.0,labelsize=14,subs='all',
            replace_nan=False,na_values=-999,
            timestep=0,xsel='mean',cyclic=False):
    """
    Parameter
    ---------------
    yy,zz  :array_like
    xsel   :{int ,string},{index of logitude,'mean'} 
    arr    :array_like
            input data
    cnum    :int or float
            the number of contour
    powerlimits:tuple
           exponent range
     subs   :{sequence of float, 'all','auto',None}
           default=(1,) ex) (1.0,2.0) 
    
    Return
    ----------------
    fig
    ax
    cbar

    """
    sformat.set_powerlimits((powerlimits))
    fig=plt.figure(figsize=(9,6),facecolor='w')
    ax=fig.add_subplot(1,1,1)
    cax=fig.add_axes([0.25,0,0.5,0.05])
    if isinstance(arr,Gtool3d):
        dat=arr.getarr(cyclic=cyclic,timestep=timestep,)[:,:,:]
    else:
        dat=arr[:,:,:]
    if xsel=='mean':
        dat=np.nanmean(dat[:,:,:],axis=2)
    else:
        dat=dat[:,:,xsel]
    set_latticks(ax=ax,dlat=dlat,labelsize=labelsize)
    if vmin is None:
        vmin=np.nanmin(dat)
    if vmax is None:
        vmax=np.nanmax(dat)
    cf=ax.contourf(yy,zz,dat
        ,vmin=vmin,vmax=vmax
        ,extend=extend
        ,cmap=cmap
        ,locator=ticker.LogLocator(subs=subs)
        ,alpha=alpha)
    cbar=fig.colorbar(cf,cax,
#        ,ticks=interval[::2]
        ticks=ticker.LogLocator(subs=(1.0,)),
        format=ticker.LogFormatterSciNotation(),
        orientation='horizontal')
    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(14)
    ax.set_ylim(1,0)
    ax.grid()
    return fig,ax,cbar
def zonal_pcolormesh(yy,zz,arr,cnum=20,clabelsize=14,extend='both',\
            cmap='viridis',alpha=1,subs=(1,),
            dlat=15.0,labelsize=14,scale='normal',vmin=None,vmax=None,
            na_values=-999,replace_nan=False,
            timestep=0,xsel='mean',cyclic=False):
    """
    Parameter
    ---------------
    yy,zz  :array_like
    xsel   :{int ,string},{index of logitude,'mean'} 
    arr    :array_like
            input data
    cnum    :int or float
            the number of contour
    powerlimits:tuple
           exponent range
     subs   :{sequence of float, 'all','auto',None}
           default=(1,) ex) (1.0,2.0) 
    
    Return
    ----------------
    fig
    ax
    cbar

    """
    sformat.set_powerlimits((-1,3))
    fig=plt.figure(figsize=(9,6),facecolor='w')
    ax=fig.add_subplot(1,1,1)
    cax=fig.add_axes([0.25,0,0.5,0.05])
    if isinstance(arr,Gtool3d):
        dat=arr.getarr(cyclic=cyclic,timestep=timestep,)[:,:,:]
    else:
        dat=arr[:,:,:]
    if xsel=='mean':
        dat=np.nanmean(dat[:,:,:],axis=2)
    else:
        dat=dat[:,:,xsel]
    set_latticks(ax=ax,dlat=dlat,labelsize=labelsize)
    if vmin is None:
        vmin=np.nanmin(dat)
    if vmax is None:
        vmax=np.nanmax(dat)
    norm={'normal':None,'log':LogNorm(vmin=vmin,vmax=vmax)}
    cf=ax.pcolormesh(yy,zz,dat
        ,cmap=cmap
        ,norm=norm[scale] 
        ,alpha=alpha)
    if scale=='log':
        cbar=fig.colorbar(cf,cax,
            ticks=ticker.LogLocator(subs=subs),
            extend=extend,
            format=ticker.LogFormatterSciNotation(),
            orientation='horizontal')
    else:
        cbar=fig.colorbar(cf,cax,extend=extend,orientation='horizontal')
    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(14)
    ax.set_ylim(1,0)
    ax.grid()
    return fig,ax,cbar


def set_axis(ax,xlabel=' ',ylabel=' ',fontsize=14,labelsize=14):
    ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel(ylabel,fontsize=fontsize)
    ax.tick_params(labelsize=labelsize,which='both')
    return ax

class MidpointNormalize(mpl.colors.Normalize):
    ## class from the mpl docs:
    # https://matplotlib.org/users/colormapnorms.html
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        super().__init__(vmin, vmax, clip)
    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))    
