# pygtool3



## pygtool

関数

### `read3d`

| Parameter | type   | description                    |
| --------- | ------ | ------------------------------ |
| file      | string | filepath for reading           |
| count     | int    | num of data,default:count=1    |
| x         | int    | num of lon grid, default:x=128 |
| y         | int    | num of lat grid, default:y=128 |
| z         | int    | num of z grid, default:z=36    |

| Return  | type                 | description      |
| ------- | -------------------- | ---------------- |
| gtool3d | pygtool_core.Gtool3d | gtool3 3D object |

### `read2d`

| Parameter | type   | description                 |
| --------- | ------ | --------------------------- |
| file      | string | filepath for reading        |
| count     | int    | num of data default:count=1 |
| x         | int    | num of lon grid, default:x=128|
| y         | int    | num of lat grid, default:y=64 |




| Return  | type                 | description      |
| ------- | -------------------- | ---------------- |
| gtool2d | pygtool_core.Gtool2d | gtool3 2D object |

### `readgrid`

| Parameter | type   | description                         |
| --------- | ------ | ----------------------------------- |
| x         | int    | num of lon grid, x=128              |
| y         | int    | num of lat grid, y=64               |
| lonfile   | string | GTAXFILE for longitude,default:None |
| latfile   | string | GTAXFILE for latitude,default:None  |

| Return    | type                   | description                    |
| --------- | ---------------------- | ------------------------------ |
| gtoolgrid | pygtool_core.GtoolGrid | used for horizontal coordinate |

引数を渡さない場合`t42`として格子を設定する。

### `readsigma`

| Parameter | type   | description                                    |
| --------- | ------ | ---------------------------------------------- |
| z         | int    | num of z grid,default:36                       |
| gtaxfile  | string | GTAXFILE for altitude,default:'GTAXLOC.HETA36' |

| Return     | type                    | description                  |
| ---------- | ----------------------- | ---------------------------- |
| gtoolsigma | pygtool_core.GtoolSigma | used for vertical coordinate |

以下はpygtoolから参照可能なモジュール

`gtplot`

`ckit`

cartopy_toolkit参照

`gtcalic`

`gtaxis`

## gtplot

### `set_lonticks`

x軸に経度を記述する

```
set_lonticks(ax,*args)
```

| Parameter | type            | description                     |
| --------- | --------------- | ------------------------------- |
| ax        | matplotlib.axes | target axes                     |
| dlon      | float           | interval of latitude,default:30 |
| labelsize | int             | fontsize of x axis,default:16   |


### `set_latticks`

x軸に緯度を記述する

```
set_latticks(ax,*args)
```

| Parameter | type            | description                     |
| --------- | --------------- | ------------------------------- |
| ax        | matplotlib.axes | target axes                     |
| dlat      | float           | interval of latitude,default:15 |
| labelsize | int             | fontsize of x axis,default:16   |

**Return**

ax

### `contourf`

```
contouf(X,Y,Z,*args)
```


| Parameter  | type                            | description                                              |
| ---------- | ------------------------------- | -------------------------------------------------------- |
| X          | numpy.ndarray                   | meshed longitude                                         |
| Y          | numpy.ndarray                   | meshed latitude                                          |
| Z          | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                               |
| cnum       | int                             | number of contour:default:20                             |
| clabelsize | int                             | fontsize of colorbar ticks                               |
| extend     | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max} |
| cmap       | string                          | カラーマップ,default:'viridis'                           |
| levels     | array_like                      | 等高線の値,default:None                                  |
| alpha      | float                           | 不透明率,{0-1},default:1                                 |
| timestep   | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0        |
| zsel       | int                             | 引数がGtool3dの時、プロットするレイヤーを指定            |
| cyclic     | bool                            | cyclic logitude or not,default:False                     |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

### `logcontourf`



```
logcontourf(X,Y,Z,*args)
```

| Parameter      | type                            | description                                              |
| -------------- | ------------------------------- | -------------------------------------------------------- |
| X              | numpy.ndarray                   | meshed logitude                                          |
| Y              | numpy.ndarray                   | meshed latitude                                          |
| Z              | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                               |
| subs           | {array_like,string,None}        | set logscaled levels{'all','auto',None},default:(1,)     |
| clabelsize     | int                             | カラーバーのfontsize:default:14                          |
| offsetTextsize | int                             | 指数のfontsize,default:14                                |
| extend         | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max} |
| cmap           | string                          | カラーマップ,default:'viridis'                           |
| vmin           | float                           | minimum value of contour range,default:None              |
| vmax           | float                           | maximum value of contour range, default:None             |
| alpha          | float                           | 不透明率,{0-1},default:1                                 |
| timestep       | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0        |
| zsel           | int                             | 引数がGtool3dの時、プロットするレイヤーを指定            |
| cyclic         | bool                            | cyclic logitude or not,default:False                     |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

### `pcolormesh`

```
pcolormesh(X,Y,Z,*args)
```
| Parameter      | type                            | description                                                  |
| -------------- | ------------------------------- | ------------------------------------------------------------ |
| X              | numpy.ndarray                   | meshed logitude                                              |
| Y              | numpy.ndarray                   | meshed latitude                                              |
| Z              | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                                   |
| scale          | string                          | select normal or log pcolormesh,{'normal','log'},default:'normal' |
| subs           | {array_like,string,None}        | set logscaled levels{'all','auto',None},default:(1,)         |
| clabelsize     | int                             | カラーバーのfontsize:default:14                              |
| offsetTextsize | int                             | 指数のfontsize,default:14                                    |
| extend         | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max}     |
| cmap           | string                          | カラーマップ,default:'viridis'                               |
| vmin           | float                           | minimum value of contour range,default:None                  |
| vmax           | float                           | maximum value of contour range, default:None                 |
| alpha          | float                           | 不透明率,{0-1},default:1                                     |
| timestep       | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0            |
| zsel           | int                             | 引数がGtool3dの時、プロットするレイヤーを指定                |
| cyclic         | bool                            | cyclic logitude or not,default:False                         |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

### `zonal_contourf`

```
zonal_contourf(X,Y,Z,*args)
```



| Parameter  | type                            | description                                                |
| ---------- | ------------------------------- | ---------------------------------------------------------- |
| X          | numpy.ndarray                   | meshed latitude                                            |
| Y          | numpy.ndarray                   | meshed altitude                                            |
| Z          | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                                 |
| cnum       | int                             | number of contour:default:20                               |
| clabelsize | int                             | fontsize of colorbar ticks                                 |
| extend     | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max}   |
| cmap       | string                          | カラーマップ,default:'viridis'                             |
| levels     | array_like                      | 等高線の値,default:None                                    |
| alpha      | float                           | 不透明率,{0-1},default:1                                   |
| timestep   | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0          |
| xsel       | {int,'mean'}                    | 切り出す経度を指定,`mean`の時東西平均をとる.default:'mean' |
| cyclic     | bool                            | cyclic logitude or not,default:False                       |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

### `zonal_logcontourf`

logスケールの東西平均断面に用いる

```
zonal_logcontourf(X,Y,Z,*args)
```

| Parameter      | type                            | description                                              |
| -------------- | ------------------------------- | -------------------------------------------------------- |
| X              | numpy.ndarray                   | meshed latitude                                  |
| Y              | numpy.ndarray                   | meshed altitude                                  |
| Z              | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                               |
| subs           | {array_like,string,None}        | set logscaled levels{'all','auto',None},default:(1,)     |
| clabelsize     | int                             | カラーバーのfontsize:default:14                          |
| offsetTextsize | int                             | 指数のfontsize,default:14                                |
| extend         | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max} |
| cmap           | string                          | カラーマップ,default:'viridis'                           |
| vmin           | float                           | minimum value of contour range,default:None              |
| vmax           | float                           | maximum value of contour range, default:None             |
| alpha          | float                           | 不透明率,{0-1},default:1                                 |
| timestep       | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0        |
| xsel       | {int,'mean'}                    | 切り出す経度を指定,`mean`の時東西平均をとる.default:'mean' |
| cyclic         | bool                            | cyclic logitude or not,default:False                     |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

### `zonal_pcolormesh`

東西平均断面のプロットに使う

```
zonal_pcolormesh(X,Y,Z,*args)
```

| Parameter      | type                            | description                                                  |
| -------------- | ------------------------------- | ------------------------------------------------------------ |
| X              | numpy.ndarray                   | meshed latitude                                              |
| Y              | numpy.ndarray                   | meshed altitude                                              |
| Z              | {numpy.ndarray,Gtool2d,Gtool3d} | model data                                                   |
| scale          | string                          | select normal or log pcolormesh,{'normal','log'},default:'normal' |
| subs           | {array_like,string,None}        | set logscaled levels{'all','auto',None},default:(1,)         |
| clabelsize     | int                             | カラーバーのfontsize:default:14                              |
| offsetTextsize | int                             | 指数のfontsize,default:14                                    |
| extend         | sting                           | 範囲外の値にコンターを描くかどうか{both,neither,min,max}     |
| cmap           | string                          | カラーマップ,default:'viridis'                               |
| vmin           | float                           | minimum value of contour range,default:None                  |
| vmax           | float                           | maximum value of contour range, default:None                 |
| alpha          | float                           | 不透明率,{0-1},default:1                                     |
| timestep       | int                             | 引数がGtoolの時のデータのtimestepを指定,default:0            |
| xsel           | {int,'mean'}                    | 切り出す経度を指定,`mean`の時東西平均をとる.default:'mean'   |
| cyclic         | bool                            | cyclic logitude or not,default:False                         |

| Return        | type               | description                                     |
| ------------- | ------------------ | ----------------------------------------------- |
| (fig,ax,cbar) | (Figure,Axes,cbar) | matplotlibのオブジェクトをtupleでまとめて返す。 |

## cartopy_toolkit

全球マップの体裁を整える関数

<https://qiita.com/earth06/items/f5958a89a546dce00c36>

### `set_geogrid`

```
set_geogrid(ax,*args)
```



| Parameter      | type            | description                                               |
| -------------- | --------------- | --------------------------------------------------------- |
| ax             | cartopy.geoaxes |                                                           |
| resolution     | string          | coastiline resolution,{'10m','50m','110m'},default:'110m' |
| dlon           | {int,float}     | interval of longitude                                     |
| dlat           | {int,float}     | interval of latitude                                      |
| xticks         | array_like      | 経度線を描く経度を手動で設定,default:None                 |
| yticks         | array_like      | 緯度線を描く経度を手動で設定,default:None                 |
| bottom         | bool            | write logitude ticklabel or not                           |
| left           | bool            | write latitude ticklabel or not                           |
| coastlinewidth | int             | 海岸線の太さ                                              |
| coastlinecolor | string          | 海岸線の色                                                |
| linewidth      | int             | 格子の太さ                                                |
| labelsize      | int             | 軸ラベルの色                                              |
| color          | string          | 格子の色                                                  |
| alpha          | float           | 格子の不透明率                                            |
| linestyle      | string          | 格子線のスタイル                                          |



### `set_feature`

```
set_feature(ax,*args)
```



## gtaxis(deprecate)



## gtcalic

### `getcmass_column`

```
getcmass_column(cmass,ps,T,sigma,sigma_M,*args)
```

| Parameter | type                    | description                                    |
| --------- | ----------------------- | ---------------------------------------------- |
| cmass     | {numpy.ndarray,Gtool3d} | mass concentration                             |
| ps        | {numpy.ndarray,Gtool2d} | surface pressure                               |
| T         | {numpy.ndarray,Gtool3d} | temperature                                    |
| sigma     | {GtoolSigma}            | vertical scale of middle grid                  |
| sigma_M   | {GtoolSigma}            | vertical scale of boudary grid                 |
| timestep  | int                     | timestep of model data                         |
| zmax      | int                     | set range of vertical integration,default:None |
| fact      | float                   | factor for adapting unit,default:1.0           |
| cyclic    | bool                    | cyclic logitutde or not,default:False          |

| Return | type          | description    |
| ------ | ------------- | -------------- |
| column | numpy.ndarray | カラム積算濃度 |



## pygtool_core

### class :`GtoolLon()`

internally used

### class :`GtoolLat()`

internally used

### class :`GtoolGrid(x=128,y=64,lonfile=None,latfile=None)`

**Method**

#### `getlonlat`

#### `getmesh`

#### `getarea`



### class :`GtoolSigma(z=36,GTAXFILE='GTAXLOC.HETA36')`

**Atribute**



**Method**

#### `get_pressure`





### class :`Gtool3d(file,x=128,y=64,z=36,count=1)`

**Atribute**



**Method**

#### `getarr`

```python
getarr(*args)
```



| Parameter   | type          | description                         |
| ----------- | ------------- | ----------------------------------- |
| timestep    | int           | model timestep                      |
| cyclic      | bool          | whether cyclic longitude or not     |
| na_values   | float         | set values treated as missing value |
| replace_nan | bool          | replace missing values or not       |
| **Return**  |               |                                     |
| arr         | numpy.ndarray |                                     |

timstepで指定された値をnumpy配列として返す。



#### `getdate`

```
getdate(*args)
```

| Parameter  | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| timestep   | int           | model timestep                       |
| timespec   | string        | default:'auto'                       |
| timeinfo   | bool          | retain time info or not,default:True |
| **Return** |               |                                      |
| arr        | numpy.ndarray |                                      |



#### `getdatetimeindex`

```
getdatetimeindex()
```

| Return   | type                 | description                                   |
| -------- | -------------------- | --------------------------------------------- |
| datetime | pandas.DatetimeIndex | 読み込んだデータすべてのdatetimeをIndexで返す |

#### `getarrays`

| Return   | type                 | description                                   |
| -------- | -------------------- | --------------------------------------------- |
| datetime | pandas.DatetimeIndex | 読み込んだデータすべてのdatetimeをIndexで返す |

#### `to_xarray`



### class :`Gtool2d(file,x=128,y=64)`

Bases: pygtool_core.Gtool3d