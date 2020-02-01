import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
import pandas as pd 
import numpy as np
import cartopy.crs as ccrs
import cartopy_toolkit as ckit

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
    dlon:float
        logitude interval:30 default
    labelsize:int 
        tick label size:16 default
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
    dlat:float
        logitude interval:15 default
    labelsize:int
        tick label size:16 default
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

def contourf(xx,yy,arr,div=20,clabelsize=14,extend='both',levels=None,cmap='viridis',powerlimits=(-1,3),alpha=1):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :array_like
            input data
    div    :int or float
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
    fig=plt.figure(figsize=(10,5),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    if levels is None:
        delta=(np.nanmax(arr)-np.nanmin(arr))/(div)
        levels=np.arange(np.nanmin(arr),abs(np.nanmax(arr))*2 +delta,delta)[0:int(div)+1]
    
    cf=ax.contourf(xx,yy,arr
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
cmap='viridis',alpha=1,extend='both',offsetTextsize=14):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :array_like
            input data
    subs   :sequence of float 'all','auto',None,
           default=(1,) ex) (1.0,2.0) 
    cmap   :string colormap
    vmin   :float minimum value(default=arr.min())
    vmax   :float maximum value(default=arr.max())
    alpha  :float 0-1 (default=1)
    extend :string {'max','min','both','neither'}
    
    
    Return
    ----------------
    fig
    ax

    """
    fig=plt.figure(figsize=(10,5),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    if vmin is None:
        vmin=arr.min()
    if vmax is None:
        vmax=arr.max()
    cf=ax.contourf(xx,yy,arr,
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
def set_axis(ax,xlabel=' ',ylabel=' ',fontsize=14,labelsize=14):
    ax.set_xlabel(xlabel,fontsize=fontsize)
    ax.set_ylabel(ylabel,fontsize=fontsize)
    ax.tick_params(labelsize=labelsize,which='both')
    return ax

import matplotlib as mpl

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
