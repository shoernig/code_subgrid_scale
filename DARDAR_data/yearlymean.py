import numpy as np
from netCDF4 import Dataset
from os import listdir
from scipy import interpolate
from time import sleep
from tqdm import tqdm
import matplotlib.pyplot as plt
import xarray as xr

ipath = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/'


#opath = ipath+'monthly/'+year+'/'

#==============
nlev = 125
nlat = 96
nlon = 192 
#==============


#=============INTERPOLATION===========================
def interpol(var,plev):

    var_int = interpolate.griddata(plev,var,lev,method='nearest')        
    return(var_int)


#==========MONTHLY MEAN=============================

def monthly_mean(var,counter):
    var_sum = np.nansum(var,0)
    counter = np.nansum(counter,0)
    mon = var_sum/np.ma.masked_equal(counter,0)
    return(mon)
#====================================================

def set_output_var(var,var_name,unit):
    #print(var_name)
    var.units = unit
    var.missing_value = np.nan
    var.long_name = var_name
    var.fill_value = np.nan
#====================================================

ipath = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/yearly/yearly_sum/'

files = listdir(ipath)

for ifile in files:
    data = xr.open_dataset(ipath+ifile)
    latitude   = data.lat[:]
    longitude  = data.lon[:]
    plev_sum   = data.plev_sum[:]
    plev_count = data.plev_count[:]
    
    iwc_sum    = data.iwc_sum[:]
    iwc_count  = data.iwc_count[:]
    
    iwp_sum      = data.iwp_sum[:]
    tiwp_sum     = data.tiwp_sum[:]
    pciwp_sum    = data.pciwp_sum[:]
    iwp_count  = data.iwp_count[:]
    
    iwc_var    = data.iwc_var[:]
    
    ta_sum     = data.ta_sum[:]
    ta_count   = data.ta_count[:]
    
    pciwc_sum   = data.pciwc_sum[:]
    pciwc_count = data.pciwc_count[:]
    
    tiwc_sum      = data.tiwc_sum[:]
    tiwc_count    = data.tiwc_count[:]
    
    total_count   = data.total_count[:]
    data.close()

    iwc   = iwc_sum/total_count
    tiwc  = tiwc_sum/total_count
    pciwc = pciwc_sum/total_count

    pres_lev  = plev_sum/plev_count
    ta        = ta_sum/ta_count

    rho   = pres_lev/(287.058*ta)

    qi   = iwc/rho
    tqi  = tiwc/rho
    pcqi = pciwc/rho 

    iwp     = iwp_sum/iwp_count
    tiwp    = tiwp_sum/iwp_count
    pciwp   = pciwp_sum/iwp_count

    var = iwc_var/(total_count)**2 - (iwc)**2

    #===========================================================================

    lev = [100000,92500,85000,77500,70000,60000,50000,40000,30000,25000,20000,15000,10000,7000,5000,3000,2000,1000,700,500,300,200,100,50,20,10]
    nlev = len(lev)

    #================INTERPOLATION=====================
    # define new interpolation variables


    qi_int          = np.zeros([nlev,nlat,nlon])
    tqi_int         = np.zeros([nlev,nlat,nlon])
    pcqi_int        = np.zeros([nlev,nlat,nlon])
    var_int      = np.zeros([nlev,nlat,nlon])

    #===========================================================================

    print('=======================================================')
    print('            INTERPOLATION                              ')
    print('=======================================================')
    for i,ik in zip(range(nlat),tqdm(range(nlat))):
        for j in range(nlon):
        
            qi_int[:,i,j]          = interpol(qi[:,i,j],pres_lev[:,i,j])     # cloud ice
            tqi_int[:,i,j]         = interpol(tqi[:,i,j],pres_lev[:,i,j])    # total cloud ice
            pcqi_int[:,i,j]        = interpol(pcqi[:,i,j],pres_lev[:,i,j])   # precipitation and convective cloud ice
            var_int[:,i,j]      = interpol(var[:,i,j],pres_lev[:,i,j])       # cloud ice variance

        sleep(0.002)

    ofile = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/yearly/'+ifile.replace('.nc','_avg.nc')
    ncout = Dataset(ofile,mode="w",format='NETCDF4_CLASSIC')
    lat  = ncout.createDimension('lat',nlat)
    lon  = ncout.createDimension('lon',nlon)
    plev = ncout.createDimension('plev',nlev)

    lons = ncout.createVariable('lon',np.float32,('lon',))
    lats = ncout.createVariable('lat',np.float32,('lat',))
    pressure = ncout.createVariable('plev',np.float32,('plev',))

    qi_mean   = ncout.createVariable('qi',np.float32, ('plev','lat','lon'))
    tqi_mean  = ncout.createVariable('tqi',np.float32, ('plev','lat','lon'))
    pcqi_mean = ncout.createVariable('pcqi',np.float32,('plev','lat','lon'))
    iwp_mean  = ncout.createVariable('iwp',np.float32, ('lat','lon'))
    tiwp_mean  = ncout.createVariable('tiwp',np.float32, ('lat','lon'))
    pciwp_mean  = ncout.createVariable('pciwp',np.float32, ('lat','lon'))
    var_mean   = ncout.createVariable('qi_var',np.float32, ('plev','lat','lon'))

    iwc_ct    = ncout.createVariable('iwc_count',np.float32, ('plev','lat','lon'))

    
    set_output_var(qi_mean, 'cloud ice mixing ratio', 'kg/kg')
    set_output_var(tqi_mean, 'total cloud ice mixing ratio', 'kg/kg')
    set_output_var(pcqi_mean, 'convective & precipitation cloud ice mixing ratio', 'kg/kg')
    set_output_var(iwp_mean, 'cloud ice water path', 'kg/m^2')
    set_output_var(tiwp_mean, 'total cloud ice water path', 'kg/m^2')
    set_output_var(pciwp_mean, 'cloud ice water path (precipiation & convection)', 'kg/m^2')
    set_output_var(var_mean, 'cloud ice variance','(kg/kg)**2')
    set_output_var(iwc_ct, 'cloud ice points','')

    lats.units      = 'degree_north'  
    lons.units      = 'degree_east'
    pressure.units  = 'Pa'

    qi_mean[:]    = qi_int
    tqi_mean[:]   = tqi_int
    pcqi_mean[:]  = pcqi_int
    iwp_mean[:]   = iwp
    tiwp_mean[:]   = tiwp
    pciwp_mean[:]   = pciwp
    var_mean[:]   = var_int
    
    

    lons[:]   = longitude[:]
    lats[:]   = latitude[:]
    pressure[:]   = lev


    ncout.close()
    print(ofile)

    



    
    

