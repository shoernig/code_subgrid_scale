#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:06:28 2023

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
#from netCDF4 import Dataset
import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap
#from mpl_toolkits.basemap import shiftgrid
import matplotlib.colors
import cmasher as cmr
import cartopy.mpl.ticker as cticker

#--------  COLOR MAP ---------
#cmap = LinearSegmentedColormap.from_list("", ["white","lightskyblue","steelblue","green","yellowgreen","yellow","gold","red","firebrick","darkred","maroon"])
#cmap =  matplotlib.colors.ListedColormap(["white","lightskyblue","skyblue","steelblue","green","yellowgreen","yellow","gold","orange","red","firebrick","darkred","maroon"])
cmap=cmr.chroma_r
#---------------------------------
plt.rcParams.update({'font.size': 30})
#-------------------------------------


letters = ['a','b','c','d','e','f','g','h','i','j','k','l']


#==============================================================================================================
ifileObs = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/monthly/DARDAR_ICON_GCM_grid_R2B04_int_v2.0_2007-2010_avg.nc'
#ifileObs = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/yearly/DARDAR_ICON_GCM_grid_R2B04_2007-2010_avg.nc'

data = xr.open_dataset(ifileObs)
lat = data.lat
lonSat = data.lon
qiSat = data.qi
plev  = data.plev
data.close()





#===============================================================================================================
ipathMod = '/work/bb1093/b380620/icon-A_out/'
EXP      = 'icon_aes_ctrl_cosp'
ifileMod = ipathMod+EXP+'/'+EXP+'_2005-2009_avg.nc'



data = xr.open_dataset(ifileMod)
lat = data.lat
lonMod = data.lon
qiMod = data.cli[0,::-1,:,:]
plev  = data.lev[::-1]
data.close()

qiMod.coords['lon'] = (qiMod.coords['lon'] + 180) % 360 - 180
qiMod = qiMod.sortby(qiMod.lon)



Diff = qiMod.values - qiSat.values
Diff = xr.DataArray(Diff,coords=qiSat.coords,dims=qiSat.dims)

#qivarMod, lonMod = shiftgrid(180.,qivarMod,lonMod,start=False)




#=============================================================================================================
opath = '/work/bb1093/b380620/plots/variance/'

nlev = 4

fig, axs = plt.subplots(nlev,3,figsize=(30,20),sharex=True,sharey=True,subplot_kw=dict(projection=ccrs.PlateCarree()))

lstart = 5

level = np.arange(0,2.2e-5,0.2e-5)

for ilev,iplot in zip(range(nlev)[::-1],range(nlev)):
    pressure = str(int(plev[ilev+lstart]/100))
    p1 = qiSat[ilev+lstart].plot(
        transform=ccrs.PlateCarree(),
        ax=axs[iplot,0],
        levels=level,
        cmap=cmap,
        add_colorbar=False,
        extend='max'
        )
    
    p2 = qiMod[ilev+lstart].plot(
        transform=ccrs.PlateCarree(),
        ax=axs[iplot,1],
        levels=level,
        cmap=cmap,
        add_colorbar=False,
        extend='max'
        )
    
    #print(qiMod[ilev+lstart])
    
    #print(qiSat[ilev+lstart])
    
    
    
    
    #Diff = qiSat[ilev+lstart] - qiMod[ilev+lstart]
    p3 = Diff[ilev+lstart].plot(
       transform=ccrs.PlateCarree(),
       ax=axs[iplot,2],
       levels=np.arange(-1.2,1.4,0.2)*1e-5,
       cmap=cmr.fusion_r,
       add_colorbar=False,
       extend='both'
       )
    
    axs[iplot,0].set_title(pressure+' hPa')
    axs[iplot,1].set_title(pressure+' hPa')
    axs[iplot,2].set_title(pressure+' hPa')
    
    axs[iplot,0].text(85,97,'DARDAR')
    axs[iplot,1].text(120,97,'ICON')
    axs[iplot,2].text(140,97,'Diff')

for ax,ilet in zip(axs.ravel(),letters):
    ax.coastlines()
    ax.text(-180,95,ilet+')')

for ax in axs.ravel()[9::]:
    # Define the xticks for longitude
    ax.set_xticks(np.arange(-180,181,120), crs=ccrs.PlateCarree())
    lon_formatter = cticker.LongitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.set_xlabel('')

for ax in axs.ravel()[::3]:
    # Define the yticks for latitude
    ax.set_yticks(np.arange(-90,91,30), crs=ccrs.PlateCarree())
    lat_formatter = cticker.LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.set_ylabel('')
    #ax.add_colorbar(False)
    

cax =  fig.add_axes([0.15,0.06,0.46,0.02])
cbar = fig.colorbar(p2,cax=cax,orientation='horizontal')
cbar.set_label('$q_i$ (kg/kg)')
fig.subplots_adjust(wspace=-0.1)  


cax =  fig.add_axes([0.65,0.06,0.23,0.02])
cbar = fig.colorbar(p3,cax=cax,orientation='horizontal')
cbar.set_label('$q_i$ (kg/kg)')
#fig.tight_layout()
#fig.text(0,0,'DARDAR')  
#plt.savefig('cli_map_korr.pdf', bbox_inches="tight")
#plt.close()
