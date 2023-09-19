#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:23:18 2023

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.colors

import numpy as np
import matplotlib.pyplot as plt

import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors
import cmasher as cmr
import cartopy.mpl.ticker as cticker


def zonal_plot(var,name,ax):
    p = ax.contourf(var.lat,var.plev/100,var[0].mean('lon'),
                    cmap = cmr.get_sub_cmap('cmr.chroma_r',0., 1.,N=len(levels)),
                    norm=norm,
                    levels=levels,
                    extend='max')
    ax.set_title(name)
    return(p)
    


levels = [0,1,2,4,8,15,20,30,40,50,60,80,100,120]
norm = colors.BoundaryNorm(boundaries=levels,ncolors=len(levels))

ifile = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/yearly/DARDAR_ICON_GCM_grid_R2B04_2007-2010_avg.nc'
letters = ['a)','b)']

fig,ax = plt.subplots(2,1,figsize=(30, 30))
ax=ax.ravel()

data = xr.open_dataset(ifile)
tqi = data.tqi *1e6
qi  = data.qi *1e6
data.close()

p1 = zonal_plot(tqi,'$q_{i,total}$',ax[0])
p2 = zonal_plot(qi,'$q_i$',ax[1])

ik = 0
for iax in ax:
    if ik == 0:
        iax.text(-100,10,'hPa')
        iax.text(95,-20,'mg/kg')

    iax.text(-88,-20,letters[ik])
    iax.invert_yaxis()
    iax.set_xticks(np.arange(-80,100,20))
    iax.set_xticklabels(['80S','60S','40S','20S','EQ','20N','40N','60N','80N'])
    ik = ik+1
    
cax = fig.add_axes([0.95,0.12,0.03,0.75])
fig.colorbar(p1,cax=cax)    




