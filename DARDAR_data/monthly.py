import numpy as np
from netCDF4 import Dataset
from os import listdir
from scipy import interpolate
from time import sleep
from tqdm import tqdm
import matplotlib.pyplot as plt
import xarray as xr

ipath = '/work/bb1093/b380620/DATA/Data/DARDAR_ICON_GCM_grid_R2B04/'


year = '2008'
files = sorted(listdir(ipath+year))

idx = []

if files[-1] == 'month':
    del (files[-1])


#print(files)


for ifile in files:
    #print(int(ifile[32:34]))
    idx.append(int(ifile[32:34]))


    
index = np.asarray(idx)
files = np.asarray(files)

jan_files = files[index==1].tolist()
feb_files = files[index==2].tolist()
mar_files = files[index==3].tolist()
apr_files = files[index==4].tolist()
may_files = files[index==5].tolist()
jun_files = files[index==6].tolist()
jul_files = files[index==7].tolist()
aug_files = files[index==8].tolist()
sep_files = files[index==9].tolist()
oct_files = files[index==10].tolist() 
nov_files = files[index==11].tolist()
dec_files = files[index==12].tolist()



# #-----------------------------------------------------
# month = '12'
# files = dec_files
# #---------------------------------------------------

opath = ipath+'monthly/'+year+'/'


# #------------------------------------------------------

#files = sorted(listdir(ipath+year))
#--------------------------------

files = [jan_files,feb_files,mar_files,apr_files,may_files,jun_files,jul_files,aug_files,sep_files,oct_files,nov_files,dec_files]

#files = [mar_files]


#-----------------------------------------------
nfiles = len(files)


month_names = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
#month_names = ['March']

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


#====================================================
print('=======================================================')
print('            READ VARIABLES & CALCULATE MEANS           ')
print('=======================================================')


for imon in range(12):
    #print(month_names[imon])
    #====================================================
    # declare variables for yearly mean
    nfiles = len(files[imon])
    lev = np.empty([nfiles,nlev,nlat,nlon])
    hgt  = np.empty([nfiles,nlev,nlat,nlon])
    
    iwc  = np.empty([nfiles,nlev,nlat,nlon])
    tiwc = np.empty([nfiles,nlev,nlat,nlon])
    pciwc= np.empty([nfiles,nlev,nlat,nlon])
    
    iwp  = np.empty([nfiles,nlat,nlon])
    tiwp  = np.empty([nfiles,nlat,nlon])
    pciwp  = np.empty([nfiles,nlat,nlon])

    iwcdar  = np.empty([nfiles,nlev,nlat,nlon])
    pciwcdar= np.empty([nfiles,nlev,nlat,nlon])
    iwpdar  = np.empty([nfiles,nlat,nlon])
    pciwpdar  = np.empty([nfiles,nlat,nlon])
    
    ta   = np.empty([nfiles,nlev,nlat,nlon])
    var = np.empty([nfiles,nlev,nlat,nlon])
    count = np.empty([nfiles,nlev,nlat,nlon])
    iwc_counter = np.empty([nfiles,nlev,nlat,nlon])
    ta_counter  = np.empty([nfiles,nlev,nlat,nlon])
    lev_counter = np.empty([nfiles,nlev,nlat,nlon])


    #print(ipath+year+'/'+files[0])

    
    for ifile,it in zip(files[imon],tqdm(range(len(files[imon])))):
    #for ifile in files[imon]:
        #print(ipath+year+'/'+ifile)
        idx = files[imon].index(ifile)
        data = xr.open_dataset(ipath+year+'/'+ifile)
    
        latitude   = data.lat[:]
        longitude  = data.lon[:]
        plev_sum   = data.plev_sum[:]
        plev_count = data.plev_count[:]
        #hgt_sum    = data.hgt_sum[:]
        #hgt_count  = data.hgt_count[:]

        # DARDAR flag

        iwcdar_sum    = data.iwcdar_sum[:]
        iwcdar_count  = data.iwcdar_count[:]

        pciwcdar_sum   = data.pciwcdar_sum[:]
        pciwcdar_count = data.pciwcdar_count[:]

        iwpdar_sum      = data.iwpdar_sum[:]
        pciwpdar_sum    = data.pciwpdar_sum[:]
        
        #--------------------------------------

        iwc_sum    = data.iwc_sum[:]
        iwc_count  = data.iwc_count[:]
    
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
        #--------------------------------------------------
    

    
        lev[idx]        = plev_sum
        lev_counter[idx] = plev_count
        
    
        iwc[idx]   = iwc_sum
        tiwc[idx]  = tiwc_sum
        pciwc[idx] = pciwc_sum
        iwp[idx]   = iwp_sum
        tiwp[idx]  = tiwp_sum
        pciwp[idx] = pciwp_sum

        iwcdar[idx]   = iwcdar_sum
        pciwcdar[idx] = pciwcdar_sum
        iwpdar[idx]   = iwpdar_sum
        pciwpdar[idx] = pciwpdar_sum
        
        count[idx] = total_count[:] 
        var[idx]   = np.ma.masked_array(iwc_var)/np.ma.masked_equal(count[idx],0) - (iwc[idx]/np.ma.masked_equal(total_count[idx],0))**2
        #var[idx]   = np.ma.masked_array(iwc_var)
    
        ta[idx]  = ta_sum
        ta_counter[idx] = ta_count
        iwc_counter[idx] = iwc_count[:]
    

    #------ monthly mean -----------
    iwc_mon = monthly_mean(iwc,count)
    tiwc_mon = monthly_mean(tiwc,count)
    pciwc_mon = monthly_mean(pciwc,count)

    iwcdar_mon = monthly_mean(iwcdar,count)
    pciwcdar_mon  = monthly_mean(pciwcdar,count)

    iwp_mon = monthly_mean(iwp,count[:,0])
    tiwp_mon = monthly_mean(tiwp,count[:,0])
    pciwp_mon = monthly_mean(pciwp,count[:,0])

    iwpdar_mon = monthly_mean(iwpdar,count[:,0])
    pciwpdar_mon = monthly_mean(pciwpdar,count[:,0])

    lev_mon = monthly_mean(lev,lev_counter)
    ta_mon  = monthly_mean(ta,ta_counter)

    #varsum_mon = monthly_mean(var,count)
    #var_mon = varsum_mon - (np.ma.masked_invalid(iwc_mon)**2)

    

    
    var_mon = np.nanmean(var,0)
    #print(var_mon[var_mon>0])
    #break
    

    #----------------------------------------------
    rho_mon = lev_mon/(287.058*np.ma.masked_equal(ta_mon,0))

    qi_mon   = iwc_mon  /rho_mon
    tqi_mon  = tiwc_mon /rho_mon
    pcqi_mon = pciwc_mon/rho_mon

    qidar_mon = iwc_mon  /rho_mon
    pcqidar_mon = pciwcdar_mon/rho_mon

    iwc_count_sum = np.nansum(iwc_counter,0)
    
    #----------------------------------------------

    var_mon = var_mon/rho_mon**2
    #======== NETCDF4 OUTPUT FILE=======================

    ofile = opath+'DARDAR_ICON_GCM_grid_R2B04_'+year+'_'+"%02d" % (imon+1)+'_avg.nc'
    ncout = Dataset(ofile,mode="w",format='NETCDF4_CLASSIC')
    lat  = ncout.createDimension('lat',nlat)
    lon  = ncout.createDimension('lon',nlon)
    plev = ncout.createDimension('plev',nlev)

    lons = ncout.createVariable('lon',np.float32,('lon',))
    lats = ncout.createVariable('lat',np.float32,('lat',))
    pressure = ncout.createVariable('plev',np.float32,('plev',))
    pres_field = ncout.createVariable('pressure',np.float32, ('plev','lat','lon'))

    
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

    iwc_ct    = ncout.createVariable('iwc_count',np.float32, ('plev','lat','lon'))

    set_output_var(pres_field, 'air pressure', 'Pa')
    
    set_output_var(qi_mean, 'cloud ice mixing ratio', 'kg/kg')
    set_output_var(tqi_mean, 'total cloud ice mixing ratio', 'kg/kg')
    set_output_var(pcqi_mean, 'convective & precipitation cloud ice mixing ratio', 'kg/kg')
    set_output_var(qidar_mean, 'cloud ice mixing ratio (DARDAR flag)', 'kg/kg')
    set_output_var(pcqidar_mean, 'convective & precipitation cloud ice mixing ratio (DARDAR flag)', 'kg/kg')
    
    set_output_var(iwp_mean, 'cloud ice water path', 'kg/m^2')
    set_output_var(tiwp_mean, 'total cloud ice water path', 'kg/m^2')
    set_output_var(pciwp_mean, 'cloud ice water path (precipiation & convection)', 'kg/m^2')
    set_output_var(iwpdar_mean, 'cloud ice water path (DARDAR flag)', 'kg/m^2')
    set_output_var(pciwpdar_mean, 'cloud ice water path (precipiation & convection) (DARDAR flag)', 'kg/m^2')
    
    set_output_var(var_mean, 'cloud ice variance','(kg/kg)**2')
    set_output_var(iwc_ct, 'cloud ice points','')

    lats.units      = 'degree_north'  
    lons.units      = 'degree_east'
    pressure.units  = 'Pa'

    qi_mean[:]    = qi_mon
    tqi_mean[:]   = tqi_mon
    pcqi_mean[:]  = pcqi_mon
    qidar_mean[:]    = qidar_mon
    pcqidar_mean[:]  = pcqidar_mon
    
    iwp_mean[:]   = np.ma.masked_invalid(iwp_mon)
    tiwp_mean[:]   = np.ma.masked_invalid(tiwp_mon)
    pciwp_mean[:]   = np.ma.masked_invalid(pciwp_mon)

    iwpdar_mean[:]   = np.ma.masked_invalid(iwpdar_mon)
    pciwpdar_mean[:]   = np.ma.masked_invalid(pciwpdar_mon)
    
    var_mean[:]   = np.ma.masked_invalid(var_mon)
    pres_field[:] = lev_mon
    iwc_ct[:]     = np.ma.masked_invalid(iwc_count_sum)

    lons[:]   = longitude[:]
    lats[:]   = latitude[:]
    pressure[:]   = range(nlev)


    ncout.close()
    print(ofile)


    #exit()
