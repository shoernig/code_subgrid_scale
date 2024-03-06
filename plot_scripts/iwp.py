#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:56:33 2024

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as colors
import xarray as xr
import cartopy.mpl.ticker as cticker
import cmasher as cmr
import matplotlib.cm as cm


plt.rcParams.update({'font.size': 35})

def comp_map_plot(ifile,invar,iname,ax):
    levels= np.arange(0,120,10)
    nlevels = len(levels)
    cmap=cmr.get_sub_cmap('cmr.chroma_r',0., 0.9,N=nlevels)
    
    data = xr.open_dataset(ifile)
    print(iname)

    lat  = data.lat[:]
    lon  = data.lon[:]
    iwp  = data[invar] *1e3
    
        
    weights = np.cos(np.deg2rad(lat))

    ax.coastlines()
    #ax.gridlines(draw_labels=True)
    norm = colors.BoundaryNorm(boundaries=levels,ncolors=len(levels))
    avg = iwp[0].weighted(weights).mean(dim={'lat','lon'}).round(2)
    
    if 'ICON' in iname:
        print(iname)
        iwp.coords['lon'] = (iwp.coords['lon'] + 180) % 360 - 180
        iwp = iwp.sortby(iwp.lon)
        
    p = ax.contourf(iwp.lon,lat,iwp[0],cmap = cmap,
                    levels = levels,
                    extend='max',
                    transform=ccrs.PlateCarree())
    
    
    
    print(avg.values)
    ax.text(-180,97,iname)
    ax.text(97,97,'av. '+str(avg.values))
    
    # Define the xticks for longitude
    ax.set_xticks(np.arange(-180,181,60), crs=ccrs.PlateCarree())
    lon_formatter = cticker.LongitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)

    # Define the yticks for latitude
    ax.set_yticks(np.arange(-90,91,30), crs=ccrs.PlateCarree())
    lat_formatter = cticker.LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    return(p)

           
def comp_map_plot_diff(DAR,ICON,ax):
    levels = np.arange(-40,45,5)
    dataDAR = xr.open_dataset(DAR)
    dataICON = xr.open_dataset(ICON)
    
    lat = dataDAR.lat
    lon = dataDAR.lon
    
    iwpDAR = dataDAR.iwp*1e3
    iwpICON = dataICON.clivi*1e3
    iwpICON.coords['lon'] = (iwpICON.coords['lon'] + 180) % 360 - 180
    iwpICON = iwpICON.sortby(iwpICON.lon)
    
    print(iwpDAR,iwpICON)

    iwp = iwpICON.values - iwpDAR.values
    iwp = xr.DataArray(iwp,coords=iwpDAR.coords,dims=iwpDAR.dims)
    print(iwp.shape)
 
        
    weights = np.cos(np.deg2rad(lat))
    avg = iwp.weighted(weights).mean(dim={'lat','lon'}).round(2)
    ax.coastlines()
    #ax.gridlines(draw_labels=True)
    norm = colors.BoundaryNorm(boundaries=levels,ncolors=len(levels))
    

    p = ax.contourf(lon,lat,iwp[0],cmap = cmr.get_sub_cmap('cmr.fusion_r',0.1, 0.9,N=len(levels)),
                    levels = levels,
                    extend='both',
                    transform=ccrs.PlateCarree())
       
     
    
    print(avg.values)
    ax.text(-180,97,'ICON-DARDAR')
    ax.text(97,97,'av. '+str(avg[0].values))
    
    # Define the xticks for longitude
    ax.set_xticks(np.arange(-180,181,60), crs=ccrs.PlateCarree())
    lon_formatter = cticker.LongitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)

    # Define the yticks for latitude
    ax.set_yticks(np.arange(-90,91,30), crs=ccrs.PlateCarree())
    lat_formatter = cticker.LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    
    return(p)


ifileDARDAR = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/monthly/DARDAR_ICON_GCM_grid_R2B04_v2.0_2007-2010_avg.nc'
ifileICON2d = '/work/bb1093/b380620/icon-A_out/icon_aes_ctrl_cosp/icon_aes_ctrl_2d_2003-2009_avg.nc'
ifileICONaggstoch2d = '/work/bb1093/b380620/icon-A_out/icon_aes_ctrl_cosp_aggstoch/icon_aes_ctrl_cosp_aggstoch_2d_2003-2009_avg.nc'


projection = ccrs.PlateCarree()

fig,ax = plt.subplots(1,3,figsize=(40,40),subplot_kw={'projection': projection})
ax = ax.ravel()

p1 = comp_map_plot(ifileDARDAR, 'iwp','a) DARDAR',ax[0])
p2 = comp_map_plot(ifileICON2d,'clivi','b) ICON',ax[1])
p3 = comp_map_plot_diff(ifileDARDAR,ifileICON2d,ax[2])
#p3 = comp_map_plot(ifileICONaggstoch2d,'clivi','AGGstoch',ax[2])

cax =  fig.add_axes([0.13,0.39,0.5,0.02])
fig.colorbar(p2,cax=cax,orientation = 'horizontal',label='CIWP (g m$^{-2}$)')

cax =  fig.add_axes([0.65,0.39,0.26,0.02])
fig.colorbar(p3,cax=cax,orientation = 'horizontal',label='CIWP (g m$^{-2}$)')
#
print('plot')
opath = '/home/b/b380620/plot_script/Paper_subgrid_scale/'
plt.savefig(opath+'iwp.pdf', bbox_inches="tight")
plt.close()