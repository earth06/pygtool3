# coding: utf-8

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LatitudeFormatter,LongitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.path as mpath
import matplotlib.pyplot as plt

def set_geogrid(ax,resolution='110m'
               ,dlon=60,dlat=30
               ,manual_ticks=False,xticks=None,yticks=None
               ,bottom=True,left=True,right=False,top=False
               ,coastlinewidth=1
               ,coastlinecolor='black'
               ,linewidth=0.5,fontsize=15,labelsize=15
               ,color='grey' ,alpha=0.8,linestyle='-' ):
    """
    parameter
    -------------
    ax        :cartopy.mpl.geoaxes
    dlon      :float  grid interval of longitude
    dlat      :float  grid interval of latitude
    linewidth,fontsize,labelsize,alpha :float
    color     :string
    resolution :string '10m','50m','110m'
    bottom    :boolean draw  xaxis ticklabel
    lfet      :boolean draw  yaxis ticklabel
    
    return 
    -------------
    ax
    """
#    labelpos=[bottom,left,top,right]
#    
#    plt.rcParams['ytick.left']=plt.rcParams['ytick.labelleft']=left
#    plt.rcParams['ytick.right']=plt.rcParams['ytick.labelright']=right
#    plt.rcParams['xtick.top']=plt.rcParams['xtick.labeltop']=top
#    plt.rcParams['xtick.bottom']=plt.rcParams['xtick.labelbottom']=bottom

    ax.coastlines(resolution=resolution,linewidth=coastlinewidth
                                       ,color=coastlinecolor)
    gl = ax.gridlines(crs=ccrs.PlateCarree()
                      , draw_labels=False,
                      linewidth=linewidth, alpha=alpha
                      , color=color,linestyle=linestyle)
    if manual_ticks == False: 
        xticks=np.arange(0,360.1,dlon)
        yticks=np.arange(-90,90.1,dlat)
    gl.xlocator = mticker.FixedLocator(xticks)    
    gl.ylocator = mticker.FixedLocator(yticks)

    if (type(ax.projection)==type(ccrs.PlateCarree())): 
        ax.set_xticks(xticks,crs=ccrs.PlateCarree())
        ax.set_yticks(yticks,crs=ccrs.PlateCarree())
    
        latfmt=LatitudeFormatter()
        lonfmt=LongitudeFormatter(zero_direction_label=True)
        ax.xaxis.set_major_formatter(lonfmt)
        ax.yaxis.set_major_formatter(latfmt)
        if (bottom==False):
            ax.xaxis.set_major_formatter(plt.NullFormatter())
        if (left==False):
            ax.yaxis.set_major_formatter(plt.NullFormatter())
        ax.axes.tick_params(labelsize=labelsize)
    return ax
def set_feature(ax,scale='110m'
              ,LAND=True,OCEAN=True,RIVERS=False,LAKES=False
              ,landalpha=0.7,landcolor=[0.9375 , 0.9375 , 0.859375]
              ,oceanalpha=0.7,oceancolor=[0.59375 , 0.71484375, 0.8828125]
              ,lakealpha=0.5,lakecolor=[0.59375 , 0.71484375, 0.8828125]
              ,riveralpha=0.5,rivercolor=[0.59375 , 0.71484375, 0.8828125]):
    '''
    set LAND ,OCEAN,RIVERS,LAKES color
    parameter
    -----------
    ax    :cartopy.mpl.geoaxes
    scale :string  '10m,50m or 110m'
    landalpha :float 0.9
    oceanlapha:float 0.8
    lakealpha :float 0.5
    riveralpha:float 0.5
    *color    :colorcode
    LAND,OCEAN:bool  fill color when True (default True)
    RIVERS,LAKES:bool as above (default False)
    return
    ----------
    ax    :as above
    '''
    if LAND:
        ax.add_feature(cfeature.LAND.with_scale(scale)
                ,alpha=landalpha
                ,facecolor=landcolor)
    if OCEAN:
        ax.add_feature(cfeature.OCEAN.with_scale(scale)
                ,alpha=oceanalpha
                ,facecolor=oceancolor)
#    ax.add_feature(cfeature.COASTLINE.with_scale(scale))
#    ax.add_feature(cfeature.BORDERS, linestyle=':')
    if LAKES:
        ax.add_feature(cfeature.LAKES.with_scale(scale)
                , alpha=lakealpha
                ,facecolor=lakecolor)
    if RIVERS:
        ax.add_feature(cfeature.RIVERS.with_scale(scale)
                ,alpha=riveralpha
                ,facecolor=rivercolor)
    return ax

def Polarmap(ax):
    """
    display cricular map
    this configure is available only in South and North Polar Stereo

    Parameter
    --------------
    ax     :cartopy.mpl.geoaxes
    """
    theta = np.linspace(0,2*np.pi,100)
    center,radius=[0.5,0.5],0.5
    verts=np.vstack([np.sin(theta),np.cos(theta)]).T
    circle=mpath.Path(verts*radius+center)

    ax.set_boundary(circle,transform=ax.transAxes)

    return ax
