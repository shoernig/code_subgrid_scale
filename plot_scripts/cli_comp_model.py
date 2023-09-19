#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:22:52 2023

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors

import numpy as np
import matplotlib.pyplot as plt

import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors
import cmasher as cmr
import cartopy.mpl.ticker as cticker


ipath = '/work/bb1093/b380620/icon-A_out/'
EXPS  = ['icon_aes_ctrl_cosp','icon_aes_ctrl_cosp_aggstoch']
names = ['CTRL','AGGstoch']
letters = ['a)','b)']

fig,ax = plt.subplots(2,1,figsize=(30, 20))
ax=ax.ravel()

for iexp,iname,iax in zip(EXPS,names,ax):
    ik = EXPS.index(iexp)
    ifile = ipath + iexp + '/'+iexp+'_2005-2009_avg.nc'
    data = xr.open_dataset(ifile)
    cli = data.cli*1e6
    data.close()
    
    if iname == names[0]:
        ref = cli
        p = iax.contourf(cli.lat,cli.lev/100,cli.mean({'time','lon'}),
                         cmap=cmr.get_sub_cmap('cmr.chroma_r',0., 0.9),
                         extend='max')
        iax.text(-100,10,'hPa')
        iax.text(95,-20,'mg/kg')
        iax.set_title(iname)
    else:
        diff = cli-ref
        proc = (cli/ref.where(ref>1e-10)-1) *100
        
        print(proc)
        
        p = iax.contourf(cli.lat,cli.lev/100,diff.mean({'time','lon'}),
                         cmap =cmr.fusion_r,
                         levels = np.arange(-1.6,1.8,0.2),
                         extend='both')
        
        #p = iax.contourf(cli.lat,cli.lev/100,proc.mean({'time','lon'}),
        #                 cmap =cmr.fusion_r,
        #                 levels = np.arange(-20,22,2),   
        #                 )
        
        iax.set_title(iname+' - '+names[0])
    iax.text(-88,-20,letters[ik])
    iax.invert_yaxis()
    iax.set_xticks(np.arange(-80,100,20))
    iax.set_xticklabels(['80S','60S','40S','20S','EQ','20N','40N','60N','80N'])
    fig.colorbar(p,ax=iax)
    
        
    














