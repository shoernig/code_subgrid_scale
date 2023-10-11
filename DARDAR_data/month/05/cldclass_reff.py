from pyhdf.SD import SD, SDC 
from pyhdf.HDF import *
from pyhdf.VS import *
import pprint
import numpy as np
import os, sys
from netCDF4 import Dataset
import scipy.interpolate as sci
from scipy import interpolate
import matplotlib.pyplot as plt
import xarray as xr
import h5py

def DARDAR_cldclass(year,day):
    
    #=============================================================================================
    def readSpecBits(arr,preskip,nbits,postskip):
        #print(arr.dtype, arr.dtype.itemsize)
        assert arr.dtype.itemsize*8==preskip+nbits+postskip, 'bit pattern do not match bit length of arr datatype'
        p = (1<<nbits)-1
        return((arr>>postskip)&p)

    def interpol(var,lev_int):
         
        var_int = interpolate.griddata(hgtDAR,var,lev_int,method='nearest')
        var_int = np.ma.masked_where(lev_int<0,var_int)
 
        return(var_int)

    def metadata(var,unit,FillValue,longname,description):
        var.units       = unit
        #var.fill_value  = FillValue
        var.long_name   = longname
        var.description = description
        #var.missing_value = FillValue
        return(var)
    #=============================================================================================



    ipath = '/work/bb1093/b380620/DATA/Data/2B-CLDCLASS/'

    daypath = ipath+year+'/'+day+'/'
    files = os.listdir(daypath)


    #----------------------------------
    ipath = '/scratch/b/b380333/share/DARDAR-Nice/DARNI_L2_PRO.v2.0/'


    daypathDAR = ipath+year+'/'+day+'/'
    filesDA   = os.listdir(daypathDAR)


    filesDAR = []
    daysq = day.replace('_','')

    filesCC = []

    print(day)
    for i in range(len(files)):
        f = 'DARNI_PRO_L2_v2.0_'+daysq+files[i][7:13]+'.nc'
        if f in filesDA:
            filesDAR.append(f)
            filesCC.append(files[i])
            print(files[i],'     ',f,'    ', files[i][7:13])

    
    #----------------------------------
    for ifile,ifileDAR in zip(filesCC,filesDAR):
        print('===============================================')
        print(daypath+ifile,ifileDAR)

        # data = xr.open_dataset(daypath+ifile, engine="h5netcdf")
        # print(data)
        # exit()
        

        f = HDF(daypath+ifile, SDC.READ)
        vs = f.vstart()
        vdata_lat  = vs.attach('Latitude')
        # vdata_lon  = vs.attach('Longitude')

        lat1 = sum(vdata_lat[:],[])

        
        
        # lon = sum(vdata_lon[:],[])
        
        

        vdata_lat.detach() # "close" the vdata
        # vdata_lon.detach() # "close" the vdata
        vs.end() # terminate the vdata interface

        f = SD(daypath+ifile,SDC.READ)
        scn = f.select('cloud_scenario').get()
        hgt = f.select('Height').get()

        hgtavg = np.mean(hgt[:],0)
        nray = scn.shape[0]
        nbin = scn.shape[1]

        time = np.arange(0,nray,1)
        #print(f)


        nc = Dataset(daypathDAR+ifileDAR,'r')
        iwc    = nc.variables['iwc'][:]
        hgtDAR = nc.variables['height'][:]
        lat    = nc.variables['lat'][:]
        lon    = nc.variables['lon'][:]
        ta     = nc.variables['ta'][:]
        plev   = nc.variables['plev'][:]
        dtime   = nc.variables['dtime'][:]
        base_time = nc.variables['base_time'][:]
        reff   = nc.variables['reffcli'][:]*1e6

        if nray != len(dtime):
            continue

        cs = readSpecBits(scn,11,4,1)

        #=========================================
        # EXTRACT CUMULUS AND CONVECTION / PRECIP
        #==========================================

        # CLASSIFICATIONS:
        #________________________________________
        # 00 - No Cloud         
        # 01 - Cirrus             
        # 02 - Altostratus      
        # 03 - Altocumulus      
        # 04 - Stratus           
        # 05 - Stratocumulus   
        # 06 - Cumulus
        # 07 - Nimbostratus     
        # 08 - Deep Convection 
        #_________________________________________

        conv_mask = np.where((cs== 8) | (cs == 6),0,1)
        #reff_mask = np.where((reff>0) | (reff<70),1,0)


        

        #==========================================
        #  INTERPOLATION
        #==========================================

        iwc_int = np.zeros(cs.shape)
        ta_int = np.zeros(cs.shape) 
        plev_int = np.zeros(cs.shape)
        reff_int = np.zeros(cs.shape)
        

        for i in range(nray):
            
            iwc_int[i,:] = interpol(iwc[i,:],hgt[i,:])
            ta_int[i,:]  = interpol(ta[i,:],hgt[i,:])
            plev_int[i,:] = interpol(plev[i,:],hgt[i,:])
            reff_int[i,:] = interpol(reff[i,:],hgt[i,:])


        reff_mask = np.where((reff_int>0) | (reff_int<50),1,0)
        
        mask_total = conv_mask * reff_mask
        mask_rem   = np.where(mask_total==1,0,1)
        
        iwc   = iwc_int * mask_total
        pciwc = iwc_int * mask_rem
        tiwc  = iwc_int

        nbins = range(nbin)

        #=============================================
            
        iwc    = np.ma.masked_less_equal(iwc,0)
        pciwc  = np.ma.masked_less_equal(pciwc,0)
        tiwc   = np.ma.masked_less_equal(tiwc,0)
        ta_int = np.ma.masked_less_equal(ta_int,0) 
        plev_int = np.ma.masked_less_equal(plev_int,0)

        #===============================================
        # NetCDF OUTPUT
        #===============================================


        opath = '/work/bb1093/b380620/DATA/Data/DARDAR_L2_cldclass_reff_flag/'
        ofile = ifileDAR.replace('DARNI_PRO_L2_v2.0','DARDAR_L2_cldclass_flag')
        ofile = opath+year+'/'+day+'/'+ofile


        if not year in os.listdir(opath):
            os.mkdir(opath+year)

        if not day in os.listdir(opath+year):
            os.mkdir(opath+year+'/'+day)

        print(ofile)

        ncout = Dataset(ofile,mode="w",format='NETCDF4_CLASSIC')

        ntime  = nray
        nh     = nbin


        times   = ncout.createDimension('time',ntime)
        Nbins   = ncout.createDimension('nbin',nh)

        Base_Time = ncout.createVariable('base_time',np.float64)
        Time    =  ncout.createVariable('dtime',np.float32,('time',))
        Lat     =  ncout.createVariable('lat',np.float32,('time',))
        Lon     =  ncout.createVariable('lon',np.float32,('time',))
        Nbin    =  ncout.createVariable('nbin',np.float32,('nbin',))
        IWC     =  ncout.createVariable('iwc',np.float32,('time','nbin'))
        PCIWC     =  ncout.createVariable('pciwc',np.float32,('time','nbin'))
        TIWC     =  ncout.createVariable('tiwc',np.float32,('time','nbin'))
        
        
        
        Temp    =  ncout.createVariable('ta',np.float32,('time','nbin'))
        Plev    =  ncout.createVariable('plev',np.float32,('time','nbin'))
        Hgt     =  ncout.createVariable('height',np.float32,('time','nbin'))

        #--- METADATA -----------------------------
        Base_Time = metadata(Base_Time,'seconds since 1970-01-01 00:00:00',-999.99,'reference time','earliest time stamp of data field for both day and night')
        Time    = metadata(Time,'s',-999.99,'difference time','actual relative time of each pixel corresponding to the reference time (see variable base_time): dtime=pixel_time-reference_time')
        
        IWC     = metadata(IWC,'kg m-3',-999.99,'mass concentration of frozen water in air','')
        PCIWC     = metadata(PCIWC,'kg m-3',-999.99,'mass concentration of frozen water in air (precipitating & convective)','')
        TIWC     = metadata(TIWC,'kg m-3',-999.99,'mass concentration of frozen water in air (total)','')
        
        Nbin  = metadata(Nbin,'',-999.99,'nbin:2B-CLDCLASS','')
        Plev    = metadata(Plev,'Pa',-999.99,'air pressure','interpolated from ECMWF reanalyses')
        Temp    = metadata(Temp,'K',-999.99,'air temperature','interpolated from ECMWF reanalyses')
        Hgt     = metadata(Hgt,'m',-999.99,'Height','')
        Lat     = metadata(Lat,'degree_north',-999.99,'latitude','')
        Lon     = metadata(Lon,'degree_east',-999.99,'longitude','')
        
        #----------------------------------------

        Base_Time[:]  = base_time
        Time[:]    = dtime[:]
        Nbin[:]    = nbins[:]
        
        IWC[:]     = iwc[:]
        PCIWC[:]   = pciwc[:]
        TIWC[:]    = tiwc[:]
        Temp[:]    = ta_int[:]
        Plev[:]    = plev_int[:]
        Lat[:]     = lat[:]
        Lon[:]     = lon[:]
        Hgt[:]     = hgt[:]

        ncout.close()
        print(ofile)
        print('=====file done=====')

#DARDAR_cldclass('2008','2008_10_12')
