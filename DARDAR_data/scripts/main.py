import os, sys
from cldclass import DARDAR_cldclass


ipath = '/work/bb1093/b380620/Data/2B-CLDCLASS/'
ipathDAR = '/work/bb1036/b380333/data/satellite/DARDAR-Nice/DARNI_L2_PRO.v1.10/'
years = os.listdir(ipath)

year = '2008'

ipath    = ipath+year
ipathDAR = ipathDAR+year
days     = os.listdir(ipath)
daysDAR  = os.listdir(ipathDAR)
#days = ['2008_06_12']
#idx = days.index(day[0]) 


for day in days:
    if day[5:7] == '01':
        print(day)
        
        if day in daysDAR:  
            DARDAR_cldclass(year,day)
            
            
            
                       
                 
            
       


