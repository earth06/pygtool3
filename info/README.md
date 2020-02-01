# pygtool

# Overview

This module enable to read gtool data format by python3 as numpy array.
gtool has been used to analysys CCSR/NIES AGCM model data.
## Description

gtool format is consist of Fortran binary.See below.

```Fortran
<4 byte header> <16 characters X 64 lines User header> <4 byte footer> <4byte header> <Fortran 4byte real array> <4byte footer>
```

`pygtool` reads this formated data and save them as object.
Then we can get array and its information by accessing to its method.

## Requirement

`numpy`
`pandas`
`matplotlib`
`xarray`
`cartopy`
## Usage

###

## Example
### draw contour from surface datab.

```python3

import pygtool
import numpy as np
impport matplotlib.pyplot as plt
import cartopy.crs as ccrs

data=pygtool.read2D('sample.dat',count=12)
arr=data.getarr(timestep=1)
xx,yy=pygtool.readgrid().getmesh()


```
## Install

## Future Plan

add simple plotting function as `gtplot`

add method to generate xarray.Dataset

add method to save np.ndarray as gtool format

## Contribution

## Licence

[MIT](https://github.com/earth06/pygtool/blob/master/LICENCE.md)

## Author

[earth06](https://github.com/earth06)
