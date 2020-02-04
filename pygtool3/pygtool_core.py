import numpy as np
import datetime
import cartopy.util as cutil
import xarray as xr
import pandas as pd
import pathlib

thisdir=str(pathlib.Path(__file__).resolve().parent)
class GtoolLon():
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,x=128,GTAXFILE=None):
        self.x=x
        if GTAXFILE is None:
            file=thisdir+'/GTAXDIR/GTAXLOC.GLON'+str(self.x)
        else:
            file=thisdir+'/GTAXDIR/'+GTAXFILE
        data=open(file,'br')
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.x)+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt)
        self.chunk = chunk
        data.close()
    def getlon(self,cyclic=False):
        lon = self.chunk[0]['arr']
        if cyclic:
            lon = np.append(lon,[360.0])
        return lon        
    def showlon(self,cyclic=False):
        lon=self.getlon(cyclic=cyclic)
        for i in range(len(lon)):
            print(i,':',lon[i])
class GtoolLat():
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,y=64,GTAXFILE=None):
        self.y=y
        if GTAXFILE is None:
            file=thisdir+'/GTAXDIR/GTAXLOC.GGLA'+str(self.y)
        else:
            file=thisdir+'/GTAXDIR/'+GTAXFILE
        data=open(file,'br')
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.y)+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt)
        self.chunk = chunk
        data.close()
    def getlat(self):
        lat = self.chunk[0]['arr']
        return lat
    def showlat(self):
        lat = self.getlat()
        for i in range(len(lat)):
            print(i,':',lat[i])
class GtoolGrid():
    def __init__(self,x=128,y=64,lonfile=None,latfile=None):
        self.x=x
        self.y=y
        self.lonfile=lonfile
        self.latfile=latfile
    def getlonlat(self,cyclic=False):
        """
        Parameter
        ----------
        cyclic : bool, default:False
            whether logitude is cyclic or not
        Return
        ----------
        lon,lat : numpy.ndarray, 1D array
        """
        lat=GtoolLat(self.y,GTAXFILE=self.latfile).getlat()
        lon=GtoolLon(self.x,GTAXFILE=self.lonfile).getlon(cyclic=cyclic)
        return lon,lat
    def getmesh(self,cyclic=False):
        """
        Parameter
        ----------
        cyclic : bool default:False
            whether logitude is cyclic or not
        Return
        ----------
        xx,yy  : numpy.ndarray, meshed longitude,latitude
        """
        x,y=self.getlonlat(cyclic=cyclic)
        xx,yy=np.meshgrid(x,y)
        return xx,yy
    def getmesh2(self):
        y=readlat(self.y).getlat()
        x=np.arange(1.40625,360.1,2.8125)
        xx,yy=np.meshgrid(x,y)
        return xx,yy
    def getarea(self,EARTH_RADIUS=6370e3):
        """
        Parameter
        ----------
        EARTH_RADIUS : float, default:6370e0[m]
        Return
        ----------
        area : numpy.ndarray, area of each grid
        """
        lon,lat=self.getlonlat(cyclic=True)
        dlon=np.deg2rad(lon[1:]-lon[:-1])
        lonaxis=dlon.shape[0]  # 128 
        lataxis=lat.shape[0]   # 64
        latm=np.zeros(lataxis+1)
        latm[1:-1]=0.5e0*(lat[0:-1]+lat[1:])
        latm[0]=90.e0
        latm[-1]=-90.0e0
        dlat=np.sin(np.deg2rad(latm[:-1]))-np.sin(np.deg2rad(latm[1:]))
        area=(EARTH_RADIUS**2)*(dlon.reshape((1,lonaxis)))*\
                dlat.reshape((lataxis,1))
        return area
class GtoolSigma():
    """
    read sigma-grid
    """

    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,z=36,GTAXFILE='GTAXLOC.HETA36'):
        self.z=z
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.z)+"f")
                       ,self.tail2])     #big endian
        file=thisdir+'/GTAXDIR/'+GTAXFILE
        with open(file,'br') as data:
            chunk=np.fromfile(data,dtype=dt,count=3)
        self.chunk = chunk
        self.ss=self.chunk[0]['arr']
        self.aa=self.chunk[1]['arr']
        self.bb=self.chunk[2]['arr']
    def get_pressure(self,ps,timestep=0,cyclic=False):
        """
        convert surface pressure to 3D pressure
        Parameter
        ------------------
        ps np.ndarray or Gtool2d , surface pressure
        Return
        ------------------
        p np.ndarray [hPa]
        """
        if isinstance(ps,Gtool2d):
            psarr=ps.getarr(cyclic=cyclic,timestep=timestep)
        else:
            psarr=ps
        lataxis,lonaxis=psarr.shape
        altaxis=self.aa.shape[0]
        P=self.aa.reshape((altaxis,1,1)) \
         +self.bb.reshape((altaxis,1,1))*psarr
        return P
class GtoolPressure():
    """
    read P-grid
    """
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    def __init__(self,z=35,GTAXFILE='GTAXLOC.AR5PL35'):
        self.z=z
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+str(self.z)+"f")
                       ,self.tail2])     #big endian
        file=thisdir+'/GTAXDIR/'+GTAXFILE
        with open(file,'br') as data:
            chunk=np.fromfile(data,dtype=dt,count=1)
        self.chunk = chunk
        self.pp=self.chunk[0]['arr']
    def get_pressure(self):
        """
        return pressure as 3D
        Parameter
        ------------------
        Return
        ------------------
        p np.ndarray,(z,1,1) [hPa]
        """
        return self.pp.reshape((self.z,1,1))
    def get_dp(self):
        """
        calculate dp = P[k+1]-P[k]
        Return
        -----------------
        dp : np.ndarray,(z-1,1,1) [hPa]
        """
        dp=self.pp[1:]-self.pp[:-1]
        return dp.reshape((self.z-1,1,1))

class Gtool3d:
    """
    read gtool format data 
    to generate this instance pass filename

    Constant value
    ---------------
    head,tail,head2,tail2 :4byte binary
             size info of fortran binary header
    Method
    --------------
    __init__(self,data,count,x,y,z)
    getarr(self,timestep)
    getheader()
    getDate 
    """
    head = ("head",">i4")
    tail = ("tail",">i4")
    head2 = ("head2",">i4")
    tail2 = ("tail2",">i4") 
    def __init__(self,file,count=1,x=128,y=64,z=36):
        """
        Parameter
        ----------------
        file  : string 
                filename of datafile
        count : int  
                num of data ex) daily=365,monthly=12
        x,y,z :int,defalt: (lon,lat,alt)=(128,64,36)
        """
        data = open(file,'br')
        self.x=x
        self.y=y
        self.z=z
        self.count=count
        if z == None:
            self.summ=str(int(x*y))
        else:
            self.summ=str(int(x*y*z))
        dt = np.dtype([self.head
                       ,("header",">64S16")
                       ,self.tail,self.head2
                       ,("arr",">"+self.summ+"f")
                       ,self.tail2])     #big endian
        chunk=np.fromfile(data,dtype=dt,count=count)
        self.chunk = chunk
        data.close()
    def getarr(self,timestep=0,cyclic=False,na_values=-999
                   ,replace_nan=False):
        """
        get ndarray(z=36,y=64,x=128)
        
        Parameters
        -------------
        timestep  :  int, default:0
                  1 origin and converted to 0 origin
        cyclic    : boolean default:False
        na_values : float default:-999
        replace_nan:boolean default:False
        Return
        ----------------
        arr    : numpy.ndarray,default:(x,y,z)=(128,64,36)
        """
        arr = self.chunk[timestep]['arr']
        arr = arr.reshape((self.z,self.y,self.x),order='C')
        if replace_nan:
            arr =np.where(arr==na_values,np.nan,arr)
#            arr[arr <= na_values] = np.nan
        if cyclic:
            arr = cutil.add_cyclic_point(arr)
#        print(self.getDate(timestep=timestep))
        return arr
    def getheader(self,timestep=0):
#        print(self.chunk[timestep]['header'])
        return  self.chunk[timestep]['header']
    def getdate(self,timestep=0,timespec='auto',timeinfo=True):
        """
        return datetime string as isoformat
        parameter
        ------------
        timstep  : int (default=0)
        timespec : string(default='auto')
        timeinfo  : boolean(default=True)
        
        return
        ---------
        label    :string isoformat
        
        """
        day=self.chunk[timestep]['header'][47].decode()
        label= datetime.datetime.strptime(day, '%Y%m%d %H%M%S ').isoformat(timespec='auto')
        if (not timeinfo):
            label=label[0:10]
        return label
    def getfortranheader_footer(self,timestep=0):
        head1=self.chunk[timestep]['head']
        head2=self.chunk[timestep]['head2']
        tail1=self.chunk[timestep]['tail']
        tail2=self.chunk[timestep]['tail2']
        return head1,head2,tail1,tail2   
    def getdatetimeindex(self):
        """
        get pd.DatetimeIndex
 
        Return
        ---------------
        datetime :pd.DatetimeIndex
        """
        datelist=[] 
        for i in range(self.count):
            datelist.append(self.getdate(timestep=i))
        return pd.to_datetime(datelist)
    def getarrays(self,cyclic=False,na_values=-999,replace_nan=False):
        """
        get all timeseries of array
        
        Parameter
        -----------
        cyclic :bool default:False
        Return
        -----------
        dataarray : numpy.ndarray, (t,z,y,x)
        """
        if cyclic:
            x = self.x+1
        else:
            x = self.x
        dataarray=np.zeros((self.count,self.z,self.y,x))
        for i in range(self.count):
            dataarray[i,:,:,:]=self.getarr(timestep=i,cyclic=cyclic,replace_nan=replace_nan,na_values=na_values) 
        return dataarray
    def to_xarray(self,lon=None,lat=None,sigma=None,cyclic=False,na_values=-999,replace_nan=False,**kwargs):
        """
        convert Gtool to xarray
        Parameter
        ---------
        lon :numpy.ndarray, array of longitude
        lat :numpy.ndarray, array of latitude
        sigma:numpy.ndarray, array of altitude
        cyclic:bool
        **kwargs:string,you can add your own attribute to xarray.DataSet
        """
        head=self.getheader()
        item=head[2].decode().strip()
        title=head[3].decode().strip()
        unit=head[15].decode().strip()
        datetime=self.getdatetimeindex()
        arrays=self.getarrays(cyclic=cyclic,na_values=na_values,replace_nan=replace_nan)
        kwargs['Convention']='COARDS'
        kwargs['title']=title
        kwargs['unit']=unit
        if self.z is None:
            values={item:(['time','lat','lon'],arrays)}
            coord_dict={'time':datetime,
                        'lat':('lat',lat,{'units':'degrees_north'}),
                        'lon':('lon',lon,{'units':'degrees_east'})}
        else:
            values={item:(['time','sigma','lat','lon'],arrays)}
            coord_dict={'time':datetime,
                        'sigma':sigma,
                        'lat':('lat',lat,{'units':'degrees_north'}),
                        'lon':('lon',lon,{'units':'degrees_east'})}
        ds = xr.Dataset(
            values,
            coords=coord_dict,
            attrs=kwargs
        )
        return ds
class Gtool2d(Gtool3d):
    """
    read surface
    Parameter
    -----------------
    file  :  string filename
    count :  totaldata number
    """
    def __init__(self,file,count=1,x=128,y=64,z=None):
        super().__init__(file,count,x,y,z)
        pass
    def getarr(self,timestep=0,cyclic=False,na_values=-999,replace_nan=False):
        """
        get ndarray((y=64,x=128))
        
        Parameters
        ----------------
        timestep  : int (default 0)
        cyclic    : bool
                default = True
                if True ,add cyclic point on 2Darray
        Return
        ----------------
        arr    : numpy.ndarray((y=64,x=128))
        """
        arr = self.chunk[timestep]['arr']
#succeed when order='C' not 'F'
        arr = arr.reshape((self.y,self.x),order='C')
        if replace_nan:
#            arr[arr <= na_values] = np.nan
            arr =np.where(arr==na_values,np.nan,arr)
        if cyclic:
            arr = cutil.add_cyclic_point(arr)
#        print(self.getDate(timestep=timestep))
        return arr
    def getarrays(self,cyclic=False,replace_nan=False,na_values=-999):
        """
        compound all timeseries into array
        
        Parameter
        -----------
        cyclic :bool default:False
        Return
        -----------
        dataarray : numpy.ndarray, (t,y,x)
        """
        if cyclic:
            x = self.x+1
        else:
            x = self.x
        dataarray=np.zeros((self.count,self.y,x))
        for i in range(self.count):
            dataarray[i,:,:]=self.getarr(timestep=i,cyclic=cyclic,na_values=na_values,replace_nan=replace_nan)
        return dataarray
def isgtoolinstance(arr,timestep=0,cyclic=False,zsel=0):
	"""
	evaluate whether first argument is Gtool* or not and return it as numpy.ndarray
	Paramter
	---------
	arr : {Gtool2d,Gtool3d,numpy.ndarray},model data
	timestep : int,default=0
	cyclic : bool,default=False
	zsel   : int,select model layer,default=0
	Return
	dat : numpy.ndarray ,  
	---------
	"""
	if isinstance(arr,Gtool3d):
		dat=arr.getarr(timestep=timestep,cyclic=cyclic)[zsel,:,:]
	elif isinstance(arr,Gtool2d):
		dat=arr.getarr(timestep=timestep,cyclic=cyclic)[:,:]
	else:
		dat=arr
	return dat
if __name__ == '__main__':
    print(str(thisdir))
    
