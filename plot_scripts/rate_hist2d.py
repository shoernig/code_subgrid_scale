#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:12:42 2023

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
import matplotlib.colors as colors
import xarray as xr
from xhistogram.xarray import histogram
import matplotlib
from matplotlib.gridspec import GridSpec
import cmasher as cmr

matplotlib.rcParams.update({'font.size': 60}) 

ipath = '/work/bb1093/b380620/icon-A_out/'
EXPS = ['icon_aes_ctrl_cosp','icon_aes_ctrl_cosp_aggstoch','icon_aes_ctrl_cosp_aggstoch']
names = ['CTRL','AGGstoch','AGGstoch - CTRL']
markers = ['o','v','x']
text = ['a','b','c','d','e','f']

cmap = cmr.horizon_r
cmap_diff = cmr.fusion_r



bin_step = 2.
cli_bins_edges   = np.arange(0,140+bin_step,bin_step)
cli_bins_centers = cli_bins_edges[0:-1]+bin_step/2

nedg = len(cli_bins_edges)

st = 10
end = 120

fig, ax = plt.subplots(2,3,figsize=(60, 35))
ax = ax.ravel()

edges_cli = np.arange(50,175,5)
edges_agg = 10**(np.arange(0.5,2.6,0.1))


for iexp, iname, iax in zip(EXPS,names,ax):
    ik = names.index(iname)
    ifile = ipath+iexp+'/'+iexp+'_2006.nc'
    #print(ifile)
    
    data = xr.open_dataset(ifile)
    agg = data.aggdiag
    cli = data.cli*1e6
    data.close()

        
    bias = abs(agg*1e6*3600)
    print(ik)
    
    hist, xedges, yedges = np.histogram2d(cli.values.ravel(),bias.values.ravel(),bins = (edges_cli,edges_agg))
    if iname == names[0]:
        ref = hist
        iax.set_ylabel('Aggregation rate \n([mg/kg hr$^{-1}$])')
    elif ik == len(EXPS)-1:
        print('diff')
        Hdiff = hist - ref
        h2 = iax.pcolormesh(xedges,yedges,Hdiff.T,cmap=cmap_diff,vmin=np.min(Hdiff),vmax=-np.min(Hdiff))
        
        
    if ik < len(EXPS)-1:
        h1 = iax.pcolormesh(xedges,yedges,hist.T,cmap=cmap,vmin=0,vmax=ref.max()-ref.max()/5)
        
    iax.text(xedges[0],yedges[-1]+ yedges[-1]/10,text[ik]+')')
    iax.set_xlim(xedges[0],xedges[-1])
    iax.set_ylim(yedges[0],yedges[-1])
    iax.set_yscale('log')
    iax.set_title(iname)
    iax.set_xlabel('cloud ice mixing ratio [mg/kg]')


for iexp, iname,iax in zip(EXPS,names,ax[len(EXPS)::]):
    ik = names.index(iname) + len(EXPS)
    ifile = ipath+iexp+'/'+iexp+'_2005-2009_avg.nc'   
    
    data=xr.open_dataset(ifile)
    agg = data.aggdiag *1e6*3600
    data.close()
    
    if ik == len(EXPS):
        ref = agg
    
    
    if ik == len(text)-1:
        diff = agg - ref
        p1 = iax.contourf(agg.lat,agg.lev/100,diff[0].mean('lon'),
                          levels=np.arange(-1.2,1.4,0.2),
                          cmap=cmr.fusion_r,
                          extend='both'
                          )
    else:
        p2 = iax.contourf(agg.lat,agg.lev/100,agg[0].mean('lon'),
                          levels=np.arange(0,6.5,0.5),
                          cmap=cmr.chroma_r,
                          extend='max'
                         )
        
    if iexp == EXPS[0]:
        iax.text(-115, 10, 'hPa')
        print(ik)
    
    iax.text(-88,-20,text[ik]+')')
    iax.invert_yaxis()
    iax.set_xticks(np.arange(-90,120,30))
    iax.set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'], rotation = 30)
    iax.set_title(iname)
    
fig.subplots_adjust(hspace=0.6) 

cax = fig.add_axes([0.13,0.48,0.48,0.03])
fig.colorbar(h1,cax=cax,orientation='horizontal')


cax = fig.add_axes([0.66,0.48,0.25,0.03])
fig.colorbar(h2,cax=cax,orientation='horizontal')

cax = fig.add_axes([0.13,0.02,0.48,0.03])
fig.colorbar(p2,cax=cax,orientation='horizontal',label='Aggregation rate [mg/kg hr$^{-1}$]')

cax = fig.add_axes([0.66,0.02,0.25,0.03])
fig.colorbar(p1,cax=cax,orientation='horizontal')
#plt.savefig('rate_comp.png')
#plt.close()
    
    
    
    
    
    
    
    
    
    
    
