import os, sys
from regrid import DARDAR_L2toL3_regrid


ipath = '/work/bb1093/b380620/Data/DARDAR_L2_cldclass_flag/'

years = os.listdir(ipath)

years = ['2006','2007','2009','2010']

ipath    = ipath+year
days     = os.listdir(ipath)


for year in years:
    ipath    = ipath+year
    days     = os.listdir(ipath)
    for day in days:
        if day[5:7] == '01':
            print(day)
            DARDAR_L2toL3_regrid(year,day)
