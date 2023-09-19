#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 13:23:06 2023

@author: b380620
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors as colors

import numpy as np
import matplotlib.pyplot as plt

import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors
import cmasher as cmr
import cartopy.mpl.ticker as cticker
import matplotlib.patches as patches

matplotlib.rcParams.update({'font.size': 40}) 

ipath = '/work/bb1093/b380620/icon-A_out/'
EXPS  = ['icon_aes_ctrl_cosp','icon_aes_ctrl_cosp_aggstoch']
names = ['CTRL','AGGstoch']
letters = ['a)','b)','c)','d)','e)','f)','g)','h)','i)','j)','k)','l)','m)','n)','o)','p)','q)','r)','s)','t)']

nvar = 8

fig,ax = plt.subplots(nvar,2,figsize=(40, 55),sharex=True)





levelsdiag = [0,0.05,0.1,0.2,0.3,0.4,0.5,1.,2.,5.,7.5,10.,12.5,15.,17.5,20.,25.]#np.arange(0,5.5,0.05)
#levelsdiagdiff = [-2,-1.5,-1.25,-1.0,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.,1.25,1.5,2.0]
levelsdiagdiff = np.arange(-1.5,1.6,0.1)
 
#ax=ax.ravel()

def zonal_plot(var,ax,levels,title,labelname):
    norm = colors.BoundaryNorm(boundaries=levels,ncolors=len(levels))
    p = ax.contourf(var.lat,var.lev/100,var.mean({'time','lon'}),
                     cmap=cmr.get_sub_cmap('cmr.chroma_r',0., 0.9,N=len(levels)),
                     levels=levels,
                     norm=norm,
                     extend='max')
    ax.text(-70,-15,title)
    fig.colorbar(p,ax=ax,label=labelname)
    return(p)
    
def zonal_plot_diff(var,ax,levels,title,labelname):
    norm = colors.BoundaryNorm(boundaries=levels,ncolors=len(levels))
    p = ax.contourf(var.lat,var.lev/100,var.mean({'time','lon'}),
                     cmap = cmr.get_sub_cmap('cmr.fusion_r',0., 1.,N=len(levels)),
                     levels = levels,
                     extend='both')
    ax.text(-70,-15,title)
    fig.colorbar(p,ax=ax,label=labelname)
    return(p)




for iexp,iname in zip(EXPS,names):
    ik = EXPS.index(iexp)
    ifile = ipath + iexp + '/'+iexp+'_2005-2009_avg.nc'
    data = xr.open_dataset(ifile)
    cli = data.cli*1e6
    agg = data.aggdiag * 1e6*3600
    aci = data.acidiag * 1e6*3600
    sed = data.seddiag * 1e6*3600
    dep = data.depdiag * 1e6*3600
    mlt = data.mltdiag * 1e6*3600
    frz = data.frldiag * 1e6*3600
    evp = data.evpdiag * 1e6*3600
    data.close()
    
    if iname == names[0]:
        refcli = cli
        refagg = agg
        refaci = aci
        refacg = aci+agg
        refsed = sed
        refdep = dep
        refmlt = mlt
        reffrz = frz
        refevp = evp
        
        zonal_plot(cli,ax[0,ik],np.arange(0,16,2),'cloud ice',' (mg/kg)')
        zonal_plot(cli,ax[1,ik],levelsdiag,'Agg (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot(aci,ax[2,ik],levelsdiag,'Aci (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot(evp,ax[3,ik],levelsdiag,'Evp (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot(mlt,ax[4,ik],levelsdiag,'Mlt (decrease)',' (mg(kg hr$^{-1}$)')
        #zonal_plot(aci+agg,ax[3,ik],levelsdiag,'Agg + Aci',' (mg(kg hr$^{-1}$)')
        zonal_plot(sed,ax[5,ik],levelsdiag,'Sed (increase)',' (mg(kg hr$^{-1}$)')
        zonal_plot(dep,ax[6,ik],levelsdiag,'Dep (increase)',' (mg(kg hr$^{-1}$)')
        zonal_plot(frz,ax[7,ik],levelsdiag,'Frz (increase)',' (mg(kg hr$^{-1}$)')

        
        #ax.text(-100,10,'hPa')
        #ax.text(95,-20,'mg/kg')
        for i in range(nvar):
            ax[i,ik].text(65,-15,iname)
            ax[i,ik].invert_yaxis()
            ax[i,ik].set_xticks(np.arange(-80,100,20))
            ax[i,ik].set_xticklabels(['80S','60S','40S','20S','EQ','20N','40N','60N','80N'])
            
        
    else:
        diffcli = cli-refcli
        diffagg = agg-refagg
        diffaci = aci-refaci
        diffacg = agg+aci - refacg
        diffsed = sed - refsed
        diffdep = dep - refdep
        diffmlt = mlt -refmlt
        diffrz = frz -reffrz
        diffevp  = evp-refevp
        
        zonal_plot_diff(diffcli,ax[0,ik],np.arange(-1.6,1.8,0.2),'cloud ice',' (mg/kg)')
        zonal_plot_diff(diffagg,ax[1,ik],levelsdiagdiff,'Agg (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffaci,ax[2,ik],levelsdiagdiff,'Aci (decrease)',' (mg(kg hr$^{-1}$)')
        #zonal_plot_diff(diffacg,ax[3,ik],levelsdiagdiff,'Agg + Aci',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffevp,ax[3,ik],levelsdiagdiff,'Evp (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffmlt,ax[4,ik],levelsdiagdiff,'Mlt (decrease)',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffsed,ax[5,ik],levelsdiagdiff,'Sed (increase)',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffdep,ax[6,ik],levelsdiagdiff,'Dep (increase)',' (mg(kg hr$^{-1}$)')
        zonal_plot_diff(diffrz,ax[7,ik],levelsdiagdiff,'Frz (increase)',' (mg(kg hr$^{-1}$)')

        
        for i in range(nvar):
           ax[i,ik].text(14,-15,iname+' - '+names[0])
           ax[i,ik].invert_yaxis()
           ax[i,ik].set_xticks(np.arange(-90,120,30))
           ax[i,ik].set_xticklabels(['90S','60S','30S','EQ','30N','60N','90N'])
           #ax[i,ik].figure(facecolor='red')
        
        
    ax[0,ik].text(-110,50,'hPa')
    
    
    #for i in np.arange(1,5,1):
    #    ax[i,ik].patch.set_facecolor('blue')
    
for ax,ilet in zip(ax.ravel(),letters):
    ax.text(-90,-15,ilet)
    ax.set_ylim(1000,0)
    ax.set_yticks(np.arange(1000,0,-200))
    bb = ax.get_window_extent()

plt.figure(facecolor='red')




        
        #p = iax.contourf(cli.lat,cli.lev/100,proc.mean({'time','lon'}),
        #                 cmap =cmr.fusion_r,
        #                 levels = np.arange(-20,22,2),   
        #                 )
        
        #ax.set_title(iname+' - '+names[0])
    #ax.text(-88,-20,letters[ik])
    #ax.invert_yaxis()
    #ax.set_xticks(np.arange(-80,100,20))
    #ax.set_xticklabels(['80S','60S','40S','20S','EQ','20N','40N','60N','80N'])
    #fig.colorbar(p,ax=ax)