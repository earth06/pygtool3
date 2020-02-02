import numpy as np
import pandas as pd
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
season=['DJF','MAM','JJA','SON']
mdays=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
reg=[   'AMN', 'AMM', 'AMS', 'AFN', 'AFS',\
        'EUR', 'CEU', 'SBR', 'IND', 'CHN',\
        'JPN', 'IDN', 'AUS', 'TLD']
head = ("head",">i4")
tail = ("tail",">i4")
head2 = ("head2",">i4")
tail2 = ("tail2",">i4") 
gthead = ("header",">64S16")

ffmt=(head,tail,head2,tail2)
mid_lon=np.arange(1.40625,360.1,2.8125)
#def lonlabel(left=):

#def latlabel(left=-90,right=90,dlat=30):
#    latlist=[]
#    for i in range(lfet,right,dlat)
def get_area(dlon=2.5e0,dlat=2.5e0):
    """
    """
    er=6370e3
    xxtmp,yytmp=np.meshgrid(np.arange(0,360,dlon),np.arange(90,-90.1,-dlat))
    area=(er**2)*(np.deg2rad(dlon)*(np.sin(np.deg2rad(yytmp[0:-1,:]))\
                                  -np.sin(np.deg2rad(yytmp[1:,:])))\
)
    return area
def read_nas(filename,header=False,na_values=-999):
    """
    reading nas file with skipping data
    return pd.Dataframe

    Parameter
    ---------
    filename :string
    header   :boolean

    Return
    ---------
    df             :pd.Dataframe
    head(optional) :list
    """
    with open(filename,'tr') as data:
        line1=data.readline()
        row=int(line1.split(',')[0])
        head=data.readlines()
    df=pd.read_csv(filename,skiprows=row-1,na_values=na_values)
    if header:
        return df,head
    else:
        return df
def normdate_to_datetime():
    """
    converting floating date into datetimeindex
    """
    return
