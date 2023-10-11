import os, sys
from cldclass_reff import DARDAR_cldclass


ipath = '/work/bb1093/b380620/DATA/Data/2B-CLDCLASS/'
ipathDAR = '/scratch/b/b380333/share/DARDAR-Nice/DARNI_L2_PRO.v2.0/'
years = os.listdir(ipath)

year = '2008'

ipath    = ipath+year
ipathDAR = ipathDAR+year
days     = os.listdir(ipath)
daysDAR  = os.listdir(ipathDAR)




for day in days:
    if day[5:7] == '03':
        print(day)
        
        if day in daysDAR:  
            DARDAR_cldclass(year,day)
            
