#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 17:11:47 2023

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

matplotlib.rcParams.update({'font.size': 40}) 

ipath = '/work/bb1093/b380620/icon-A_out/'
EXPS = ['icon_aes_ctrl','icon_aes_agg_stoch','icon_aes_agg_stoch_sample']
names = ['CTRL','AGGstoch','AGGsample']
colors = ['black','orange','C0']
markers = ['--','-','-.']

cmap = cmr.horizon_r


plt.figure(figsize=(30,20))

bin_step = 2.
cli_bins_edges   = np.arange(20,130+bin_step,bin_step)
cli_bins_centers = cli_bins_edges[0:-1]+bin_step/2

nedg = len(cli_bins_edges)

st = 10
end = 50

fig = plt.figure(figsize=(30, 20))
gs = GridSpec(nrows=3, ncols=2)

ax0 = fig.add_subplot(gs[:, 0])
edges_cli = cli_bins_edges#np.arange(20,135,5)
edges_agg = 10**(np.arange(-0.6,2.8,0.2))

letters = ['b)','c)','d)']


for iexp, iname in zip(EXPS,names):
    ik = EXPS.index(iexp)
    ifile = ipath+iexp+'/'+iexp+'_1990.nc'
    
    print(ifile)
    
    data = xr.open_dataset(ifile)
    agg = data.aggdiag
    cli = data.cli*1e6
    data.close()

        
    bias = abs(agg*1e6*3600)
    
    bias_bins = []
    bias_max = []
    bias_min = []
    std = []
    
    #h = histogram(bias,bins=cli_bins_edges)

    for ibin in range(nedg-1):
        bias_bins.append(bias.where((cli>cli_bins_edges[ibin])&(cli<cli_bins_edges[ibin+1])).mean().values)
        print(cli_bins_centers[ibin])
        #std.append(bias.where((cli>cli_bins_edges[ibin])&(cli<cli_bins_edges[ibin+1])).std().values)
        #bias_min.append(bias_bins[ibin]-std[ibin])
        #bias_max.append(bias_bins[ibin]+std[ibin])
        #bias_max.append(bias.where((cli>cli_bins_edges[ibin])&(cli<cli_bins_edges[ibin+1])).max())
        #bias_min.append(bias.where((cli>cli_bins_edges[ibin])&(cli<cli_bins_edges[ibin+1])).min())
        


        #print(cli_bins_centers[ibin],len(bias[mask]))
    
    
    

    ax0.plot(cli_bins_centers,bias_bins,markers[ik],linewidth=8.,label=names[ik],color=colors[ik])
    ax0.text(0,122,'a)')
    
    
    ax = fig.add_subplot(gs[ik,1])
    
    if ik == 0:
        hist, xedges, yedges = np.histogram2d(cli.values.ravel(),bias.values.ravel(),bins = (edges_cli,edges_agg))
        ref = hist
        p1 = ax.pcolormesh(xedges,yedges,hist.T,cmap=cmap)
        ax.set_title(iname)
    else:
        hist, xedges, yedges = np.histogram2d(cli.values.ravel(),bias.values.ravel(),bins = (edges_cli,edges_agg))
        diff = hist - ref
        p2 = ax.pcolormesh(xedges,yedges,diff.T,cmap=cmr.fusion_r,vmin=diff.min(),vmax = -diff.min())
        ax.set_title(iname+' - '+names[0])
    
    
    ax.text(xedges[0],yedges[-1]+50,letters[ik])   
    ax.set_xlim(xedges[0],xedges[-1])
    ax.set_ylim(edges_agg[0],edges_agg[-1])
    ax.set_yscale('log')
    
    
    if ik != len(EXPS)-1:
        ax.tick_params(axis='x',which='both',bottom=False, top=False, labelbottom=False)
       
    else:
        ax.set_xlabel('cloud ice mixing ratio [mg/kg]')
        
        
        
    ax.set_ylabel('Aggregation rate \n[mg/kg hr$^{-1}$]')
    #plt.fill_between(cli_bins_centers, bias_min,bias_max,alpha=0.45,color=colors[ik])
    #plt.plot(cli_bins_centers,h,linewidth=3.,label=names[ik])

    ax0.set_ylabel('Aggregation rate [mg/kg hr$^{-1}$]')
    ax0.set_xlabel('cloud ice mixing ratio [mg/kg]')
    ax0.legend(loc='upper left')
    ax0.grid(True)
    
  
    ax0.set_xlim(cli_bins_centers[0],cli_bins_centers[-1])
    ax0.set_yscale('log')
    ax0.set_ylim(edges_agg[0],edges_agg[-1])

fig.subplots_adjust(wspace=0.3) 

cax = fig.add_axes([0.925,0.657,0.02,0.223])
fig.colorbar(p1,cax=cax)

cax = fig.add_axes([0.925,0.13,0.02,0.47])
fig.colorbar(p2,cax=cax)
#plt.savefig('bias_rate_comp.png')
#plt.close()
