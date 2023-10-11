import numpy as np
from netCDF4 import Dataset
from os import listdir
from scipy import interpolate
from time import sleep
from tqdm import tqdm
import matplotlib.pyplot as plt
import xarray as xr

#====================================================

def set_output_var(var,var_name,unit):
    #print(var_name)
    var.units = unit
    var.missing_value = np.nan
    var.long_name = var_name
    var.fill_value = np.nan


#=============INTERPOLATION===========================
def interpol(var,plev):
    
    var_int = interpolate.griddata(plev,var,lev,method='nearest')
    
    return(var_int)

#====================================================


ifile = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/monthly/DARDAR_ICON_GCM_grid_R2B04_v2.0_2007-2010_avg.nc' #INPUT FILE


data = xr.open_dataset(ifile)
qi = data.qi[0]
pcqi = data.pcqi[0]
tqi = data.tqi[0]
pressure = data.pressure[0]

# DARDAR PRECIP FLAG
qidar = data.qidar[0]
pcqidar = data.pcqidar[0]
#=======================

qi_var = data.qi_var[0]



nlat = len(data.lat)
nlon = len(data.lon)

#--------------------------------------------------------------  
lev = [100000,92500,85000,77500,70000,60000,50000,40000,30000,25000,20000,15000,10000,7000,5000,3000,2000,1000,700,500,300,200,100,50,20,10]
nlev = len(lev)   
#--------------------------------------------------------------

#================INTERPOLATION=====================
# define new interpolation variables


# iwc_int          = np.zeros([nlev,nlat,nlon])
# pciwc_int        = np.zeros([nlev,nlat,nlon])
# tiwc_int         = np.zeros([nlev,nlat,nlon])

var_int    = np.zeros([nlev,nlat,nlon])

qi_int        = np.zeros([nlev,nlat,nlon])
tqi_int       = np.zeros([nlev,nlat,nlon])
pcqi_int      = np.zeros([nlev,nlat,nlon])

qidar_int  = np.zeros([nlev,nlat,nlon])
pcqidar_int      = np.zeros([nlev,nlat,nlon])

# rho_int = np.zeros([nlev,nlat,nlon])
# ta_int  = np.zeros([nlev,nlat,nlon])

# hgt_int = np.zeros([nlev,nlat,nlon])

#==================================================
# ---------------------------------------------------------------



print('=======================================================')
print('            INTERPOLATION                              ')
print('=======================================================')
for i,ik in zip(range(nlat),tqdm(range(nlat))):
    for j in range(nlon):
        qi_int[:,i,j] = interpol(qi[:,i,j], pressure[:,i,j])
        tqi_int[:,i,j] = interpol(tqi[:,i,j], pressure[:,i,j])
        pcqi_int[:,i,j] = interpol(pcqi[:,i,j], pressure[:,i,j])
        var_int[:,i,j]      = interpol(qi_var[:,i,j], pressure[:,i,j])       # cloud ice variance

        qidar_int[:,i,j] = interpol(qidar[:,i,j], pressure[:,i,j])
        pcqidar_int[:,i,j] = interpol(pcqidar[:,i,j], pressure[:,i,j])

# ==== OUTPUT FILE =====================================
ofile = ifile.replace('v2.0','int_v2.0')
print(ofile)

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
qidar_mean   = ncout.createVariable('qidar',np.float32, ('plev','lat','lon'))
pcqidar_mean = ncout.createVariable('pcqidar',np.float32,('plev','lat','lon'))


iwp_mean  = ncout.createVariable('iwp',np.float32, ('lat','lon'))
tiwp_mean  = ncout.createVariable('tiwp',np.float32, ('lat','lon'))
pciwp_mean  = ncout.createVariable('pciwp',np.float32, ('lat','lon'))
iwpdar_mean  = ncout.createVariable('iwpdar',np.float32, ('lat','lon'))
pciwpdar_mean  = ncout.createVariable('pciwpdar',np.float32, ('lat','lon'))


var_mean   = ncout.createVariable('qi_var',np.float32, ('plev','lat','lon'))

#iwc_ct    = ncout.createVariable('iwc_count',np.float32, ('plev','lat','lon'))

    
set_output_var(qi_mean, 'cloud ice mixing ratio', 'kg/kg')
set_output_var(tqi_mean, 'total cloud ice mixing ratio', 'kg/kg')
set_output_var(pcqi_mean, 'convective & precipitation cloud ice mixing ratio', 'kg/kg')
set_output_var(qidar_mean, 'cloud ice mixing ratio (DARDAR flag)', 'kg/kg')
set_output_var(pcqidar_mean, 'convective & precipitation cloud ice mixing ratio (DARDAR flag)', 'kg/kg')


set_output_var(iwp_mean, 'cloud ice water path', 'kg/m^2')
set_output_var(tiwp_mean, 'total cloud ice water path', 'kg/m^2')
set_output_var(pciwp_mean, 'cloud ice water path (precipiation & convection)', 'kg/m^2')

set_output_var(iwpdar_mean, 'cloud ice water path', 'kg/m^2 (DARDAR flag)')
set_output_var(pciwpdar_mean, 'cloud ice water path (precipiation & convection) (DARDAR flag)', 'kg/m^2')
set_output_var(var_mean, 'cloud ice variance','(kg/kg)**2')



#set_output_var(iwc_ct, 'cloud ice points','')

lats.units      = 'degree_north'  
lons.units      = 'degree_east'
pressure.units  = 'Pa'

qi_mean[:]    = qi_int
tqi_mean[:]   = tqi_int
pcqi_mean[:]  = pcqi_int
qidar_mean[:]    = qidar_int
pcqidar_mean[:]  = pcqidar_int

iwp_mean[:]   = data.iwp
tiwp_mean[:]   = data.tiwp
pciwp_mean[:]   = data.pciwp
iwpdar_mean[:]   = data.iwpdar
pciwpdar_mean[:]   = data.pciwpdar

var_mean[:]   = var_int
    
    

lons[:]   = data.lon
lats[:]   = data.lat
pressure[:]   = lev


print('###############################')
print('FILE IS DONE')
print('###############################')
