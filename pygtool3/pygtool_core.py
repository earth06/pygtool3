import numpy as np
import datetime
import cartopy.util as cutil
import xarray as xr
import pandas as pd
import pathlib

thisdir=str(pathlib.Path(__file__).resolve().parent)
class Gtool():
    """
    set up gtool format for creating gtool emission data
    """
    head = ("head",">i")
    tail = ("tail",">i")
    head2 = ("head2",">i")
    tail2 = ("tail2",">i")
    index={'id':0,'dataset':1,'var':2,
                  'title1':13,'title2':14,'unit':15,
                  'time':24,'date':25,'utim':26,
                  'xaxis':28,'x1':29,'x2':30,
                  'yaxis':31,'y1':32,'y2':33,
                  'zaxis':34,'z1':35,'z2':36,
                  'cdate':59,'mdate':61,'msign':62,'size':63}
    def __init__(self,x=128,y=64,z=36):
        self.x=x
        self.y=y
        self.z=z
        self.num=x*y*z
        dt = np.dtype([self.head
                   ,("header",">64S16")
                   ,self.tail,self.head2
                   ,("arr",">"+str(self.num)+"f")
                   ,self.tail2])     #big endian
        data=np.zeros(1,dtype=dt)
        data['head']=1024
        data['tail']=1024
        data['head2']=self.num*4
        data['tail2']=self.num*4
        self.data=data
    def set_sampleheader(self,sample=None):
        """
        set gtool header from other sample file

        Parameters
        ----------
        sample :np.ndarray
            Gtool header from other file
        """
        self.data['header']=sample
        return 0
    def set_header(self,dataset='dataset',varname='var',title='title',\
                 unit='kg/m2',author='unknown'):
        """
        edit header

        Parameters
        ----------
        dataset :string, default 'dataset'
            dataset name such as GFED,NCEP etc...
        varname :string, default 'var'
            variable name of the data such as BCFLX
        title :string, default 'title'
            title of the data
        unit :string, default 'kg/m2'
            unit of the data
        author :string, default 'unkown'
            author of the data
        """
        self.data['header'][0,self.index['dataset']]='{:<16}'.format(dataset)
        self.data['header'][0,self.index['var']]='{:<16}'.format(varname)
        self.data['header'][0,self.index['title']]='{:<16}'.format(title[0:16])
        self.data['header'][0,self.index['title2']]='{:<16}'.format(title[16:32])
        self.data['header'][0,self.index['unit']]='{:<16}'.format(unit)
        now=datetime.datetime.now().strftime('%Y%m%d %H0000 ')
        self.data['header'][0,self.index['mdate']]='{:<16}'.format(now)
        self.data['header'][0,self.index['author']]='{:<16}'.format(author)
    def set_datetime(self,datetime='19790101 000000 ',fmt='%Y%m%d 000000 '):
        """
        set datetime

        Parameters
        ----------
        datetime :pandas.Timestamp or string('YYYYMMDD hhmmss ')
            datetime label of gtool header
        fmt :string,deafult='%Y%m%d 000000 '
            fomatter when write datetime on gtool header
        """
        if isinstance(datetime,pd.Timestamp):
            dt=datetime.strftime(fmt)
        else:
            dt=datetime
        self.data['header'][0,self.index['date']]='{:<16}'.format(dt)
    def set_values(self,arr):
        """
        set values

        Parameters
        ----------
        arr :np.ndarray
            targets data which converted to gtool
        """
        self.data['arr']=arr.astype('f4').flatten(order='C')
        return 0
    def get_data(self):
        return self.data
    def to_gtool(self,file='gtool.out',datalist=None,datetimeindex=None):
        """
        save data as gtool format

        Parameters
        ----------
        file :string,default='gtool.out'
            file name of output
        datalist :list
            list of array which has only one timestep model data
        datetimeindex :pd.Datetimeindex or list
            datetime of the model data
        """
        with open(file,'ba') as f:
            for dt,array in zip(datetimeindex,datalist):
                self.set_datetime(dt)
                self.set_values(array)
                self.data.tofile(f)
       
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
    """
    manipulate horizontal coordinate
    """
    def __init__(self,x=128,y=64,lonfile=None,latfile=None):
        self.x=x
        self.y=y
        self.lonfile=lonfile
        self.latfile=latfile
    def getlonlat(self,cyclic=False):
        """
        return horizontal coordinate

        Parameters
        ----------
        cyclic :bool, default=False
            whether logitude is cyclic or not

        Returns
        -------
        lon,lat :numpy.ndarray, 
            longitue and latitude 1D array
        """
        lat=GtoolLat(self.y,GTAXFILE=self.latfile).getlat()
        lon=GtoolLon(self.x,GTAXFILE=self.lonfile).getlon(cyclic=cyclic)
        return lon,lat
    def getmesh(self,cyclic=False):
        """
        extend logitude and latitude to 2D        

        Parameters
        ----------
        cyclic :bool default=False
            whether logitude is cyclic or not

        Returns
        -------
        xx,yy  :numpy.ndarray
            meshed longitude and latitude which are used for plot
        """
        x,y=self.getlonlat(cyclic=cyclic)
        xx,yy=np.meshgrid(x,y)
        return xx,yy
#    def getmesh2(self):
#        """
#        """
#        y=readlat(self.y).getlat()
#        x=np.arange(1.40625,360.1,2.8125)
#        xx,yy=np.meshgrid(x,y)
#        return xx,yy
    def getarea(self,EARTH_RADIUS=6370e3):
        """
        calculate area of each grid        

        Parameters
        ----------
        EARTH_RADIUS :float, default=6370e0
            earth radius[m]

        Returns
        -------
        area :numpy.ndarray 
            area of each grid[m]
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
    You can declare this class when you set sigma coordinate file
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
        extend surface pressure to 3D pressure by hydrostatic equilibrium

        Parameters
        ----------
        ps :np.ndarray or Gtool2d
            surface pressure
        timestep :int, default 0
            model timestep
        cyclic :bool, default False
            whether make logitude cyclic or not

        Returns
        -------
        p :np.ndarray
            pressure[Pa]
        """
        if isinstance(ps,Gtool2d):
            psarr=ps.getarr(cyclic=cyclic,timestep=timestep)
        else:
            psarr=ps
        lataxis,lonaxis=psarr.shape
        altaxis=self.aa.shape[0]
        P=self.aa.reshape((altaxis,1,1)) \
         +self.bb.reshape((altaxis,1,1))*psarr
        return P*1e2
    def get_dp(self,ps,timestep=0,cyclic=False):
        """
        convert surface pressure to 3D pressure

        Parameters
        ----------
        ps :np.ndarray or Gtool2d
            surface pressure
        cyclic :bool,default=False
            whether make longitude cyclic or not
        timestep :int,default=0
            model timestep

        Returns
        -------
        dp :np.ndarray
            deltaP=P[k+1]-P[K](<0)[Pa]
        """
        if isinstance(ps,Gtool2d):
            psarr=ps.getarr(cyclic=cyclic,timestep=timestep)
        else:
            psarr=ps
        lataxis,lonaxis=psarr.shape
        altaxis=self.aa.shape[0]
        PM=self.aa.reshape((altaxis,1,1)) \
         +self.bb.reshape((altaxis,1,1))*psarr
        dp=(PM[1:,:,:]-PM[0:-1,:,:])*1e2
        return dp

class GtoolPressure():
    """
    read P-grid

    Parameters
    ----------
    z :int,default 35
        num of vertical grid
    GTAXFILE :string, default GTAXLOC.AR5PL35
        file of vertical coordinate

    Attributes
    ----------
    z :int 
        num of vertical grid
    pp :numpy.ndarray
        1D array of pressure
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

        Returns
        -------
        p :np.ndarray,(z,1,1) [hPa]
            pressure
        """
        return self.pp.reshape((self.z,1,1))
    def get_dp(self):
        """
        calculate dp

        Returns
        -------
        dp :np.ndarray,
            dp = P[k+1]-P[k] [hPa]
        """
        dp=self.pp[1:]-self.pp[:-1]
        return dp.reshape((self.z-1,1,1))

class Gtool3d:
    """
    read gtool format data 
    to generate this instance pass filename

    Attributes
    ----------
    head,tail,head2,tail2 :4byte binary
        size info of fortran binary header
    """
    head = ("head",">i4")
    tail = ("tail",">i4")
    head2 = ("head2",">i4")
    tail2 = ("tail2",">i4") 
    def __init__(self,file,count=1,x=128,y=64,z=36):
        """
        Parameters
        ----------
        file  :string 
            filename of datafile
        count :int  
            the number of data 
        x,y,z :int,defalt (x,y,z)=(128,64,36)
            the number of each coordinate
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
        return model data as array
        
        Parameters
        ----------
        timestep  :int, default 0
            model timestep
        cyclic    :boolean, default False
            whether make logitude cyclic or not
        na_values :float, default -999
            set value which is treated as missing value
        replace_nan :boolean, default False
            whether replace na_valuse into NaN or not

        Returns
        -------
        arr    :numpy.ndarray, default (x,y,z)=(128,64,36)
            model data
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
        return datetime as isoformat

        Parameters
        ----------
        timstep  :int, default 0
            model timestep
        timespec :string, default 'auto'
        timeinfo  :boolean, default True

        Returns
        -------
        label    :string
            isoformated datetime

        """
        day=self.chunk[timestep]['header'][47].decode()
        label= datetime.datetime.strptime(day, '%Y%m%d %H%M%S ').isoformat(timespec='auto')
        if (not timeinfo):
            label=label[0:10]
        return label
    def getfortranheader_footer(self,timestep=0):
        """
        return fortran header footer

        Returns
        -------
        h1,h2,t1,t2 :tuple of int
            4byte integer
        """
        h1=self.chunk[timestep]['head']
        h2=self.chunk[timestep]['head2']
        t1=self.chunk[timestep]['tail']
        t2=self.chunk[timestep]['tail2']
        return h1,h2,t1,t2   
    def getdatetimeindex(self):
        """
        return  datetimeindex of read file

        Returns
        -------
        datetime :pd.DatetimeIndex
            datetimeindex of read file
        """
        datelist=[] 
        for i in range(self.count):
            datelist.append(self.getdate(timestep=i))
        return pd.to_datetime(datelist)
    def set_datetimeindex(self,datetime=None):
        """
        set datetimeindex
        
        Parameters
        -----------
        datetime :pd.DatetimeIndex or None, default None
            set datetimeindex. set datetimeindex automatilcally when no argment is passed.
        """
        if datetime is None:
            self.datetimeindex=self.getdatetimeindex()
        else:
            self.datetimeindex=datetime
    def getarrays(self,cyclic=False,na_values=-999,replace_nan=False):
        """
        get  all model data in read file

        Parameters
        ----------
        cyclic :boolean, default False
            whether make logitude cyclic or not
        na_values :float, default -999
            set value which is treated as missing value
        replace_nan :boolean, default False
            whether replace na_valuse into NaN or not

        Returns
        -------
        dataarray : numpy.ndarray 
            model data but axis 0 has time
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

        Parameters
        ----------
        lon :numpy.ndarray
            array of longitude
        lat :numpy.ndarray
            array of latitude
        sigma :numpy.ndarray
            array of altitude
        cyclic :boolean
            whether make logitude cyclic or not
        na_values :float, default -999
            set value which is treated as missing value
        replace_nan :boolean, default False
            whether replace na_valuse into NaN or not
        **kwargs :string
            you can add your own attribute to xarray.DataSet

        Returns
        -------
        ds :xarray.Dataset
        """
        head=self.getheader()
        item=head[2].decode().strip()
        title=head[3].decode().strip()
        unit=head[15].decode().strip()
        datetime=self.datetimeindex
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
    read surface model data

    Parameters
    ----------
    file  :string
        filename
    count :int
        the number of data
    """
    def __init__(self,file,count=1,x=128,y=64,z=None):
        super().__init__(file,count,x,y,z)
        pass
    def getarr(self,timestep=0,cyclic=False,na_values=-999,replace_nan=False):
        """
        get ndarray((y=64,x=128))

        Parameters
        ----------
        timestep  :int ,default 0
        cyclic    :boolean, default = True
            whether make logitude cyclic or not
        na_values :float, default -999
            set value which is treated as missing value
        replace_nan :boolean, default False
            whether replace na_valuse into NaN or not

        Returns
        -------
        arr    :numpy.ndarray
            model data
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
        compound all timeseries into one array
        
        Parameters
        ----------
        cyclic :bool, default False
            whether make longitude cyclic or not 

        Returns
        -------
        dataarray :numpy.ndarray
            model values but axis 0 is time
        """
        if cyclic:
            x = self.x+1
        else:
            x = self.x
        dataarray=np.zeros((self.count,self.y,x))
        for i in range(self.count):
            dataarray[i,:,:]=self.getarr(timestep=i,cyclic=cyclic,na_values=na_values,replace_nan=replace_nan)
        return dataarray
def isgtoolinstance(arr,timestep=0,cyclic=False,zsel=0,replace_nan=False,na_values=-999):
	"""
	evaluate whether first argument is Gtool* instance 
    and return it as numpy.ndarray

	Parameters
	----------
	arr :Gtool2d or Gtool3d or numpy.ndarray
        model data
	timestep :int, default 0
        model timestep
	cyclic :boolean, default False
        whether make logitude cyclic or not
	zsel :int, default 0
        select model layer

	Returns
    -------
	dat :numpy.ndarray
        model values
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
    
