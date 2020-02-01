# pygtool3

## Overview(概要)

大気循環モデルAGCM5(CCSR/NIES)のI/Oルーチンで利用されているgtool3形式のデータを解析するライブラリです。

## Description(詳細)

gtool3形式のデータは以下の構造をとっている。

```fortran
<4byte> !FORTRAN header
<16 characters X 64 lines>　!data discription
<4byte>!FORTRAN fooder
<4byte>
<4byte array> !model raw data
<4byte>
```

基本的にはこれをnumpyで読み取ることでpythonから、データの解析、プロットを可能にしています。`pygtool3`では、これをさらに発展させ、ヘッダー情報を含めた独自のクラス定義に基づくインスタンスをして値を返却します。これによってより柔軟な解析を簡潔なコードで実現しています。

## Demo()

```python
grid=pygtool.readgrid()
xx,yy=grid.getmesh()
t=pygtool.read3d('./sampledata/T.clim',count=4)
pygtool.gtplot.contourf(xx,yy,bc.getarr()[0,:,:])
```

![](./test/sample.png)

## Requirement

python >=3.6

numpy

pandas

matplotlib

cartopy

xarray

これらが正常にインストールされていれば、おそらく大丈夫です。

## Usage

プロットに使う際は、モデルデータの読み込みに加え、格子情報のデータも読み込んでおく必要があります。

### import

パッケージ化せずに使う場合は`sys`でモジュールサーチパスを追加してからimportしてください。(こっちの方が安全かもです)

```python
import sys
sys.path.append('pygtool3')
import pygtool
```

pythonのパッケージに追加した場合は直接importできます

(まだsetup.sh書いていない...)

```python
import pygtool
```

### reading model data(モデルデータの読み込み)

gtool3形式はFORTRANバイナリを直接ファイルに書き込んでいるようなものなので、netcdf4やHDF5のようにself-describedなデータ形式ではありません。そのため読み込みの際には、モデルの出力の次元(2D or 3D)、それぞれの軸の格子の数、データの総数を知っておく必要があります。誤った値を設定すると、格納するデータが意味不明な値になります。

返り値は`pygtool_core.Gtool*`クラスとなっています。

#### read 2D data(2次元)

```python
surface_pressure=pygtool.read2d('ps',count=4)
```

第１引数はファイルパス、`count`:データの総数

x,yで格子の数を指定する。デフォルトでは(x,y)=(128,64)

#### read 3D data(3次元)

```python
temperature=pygtool.read3d('t',count=4)
```

2次元のときと同様。格子はx,y,zで指定する。デフォルトで(x,y,z)=(128,64,36)

#### reading grid data(格子情報の読み込み)

格子情報のデータを読み取り、緯度(lat)、経度(lon)、標準化高度(sigma)をそれぞれ`numpy.ndarray`として変数に代入します。

```python
# horizontal
geogrid=pygtool.readgrid()# defaultの格子情報を使う場合
#t85を用いる場合
#geogrid=pygtool.readgrid(x=256,y=128
#			,lonfile='GTAXLOC.GLON256'
#           ,latfile='GTAXLOC.GGLA128')
lon,lat=geogrid.getlonlat()
xx,yy=geogrid.getmesh()
area=geogrid.getarea()
```

`lon`,`lat`はそれぞれ(128,),(64,)の1次元配列

`xx`,`yy`は`lon`,`lat`を2次元配列に拡張したもので、プロットの際に必要です

`area`は格子の面積を表す2次元配列で、領域平均を計算したりする場合に使います。

defaultの解像度は`t42`となっています。もし変更する場合は`readgrid()`にx,y,lonfile,latfileを設定してください。

```python
# vertical
sigma=pygtool.readsigma() #default
#sigma=pygtool.readsigma(z=57,
#      gtaxfile='GTAXLOC.CETA57')
```

デフォルトでは`gtaxfile=GTAXLOC.HETA36,z=36`となっています。

### plotting(プロット)

#### calculation()



## Install

## Contribution

## License
[MIT](https://github.com/earth06/pygtool3/blob/master/info/LICENCE.md)

## Author
[earth06](https://github.com/earth06)

## Document



