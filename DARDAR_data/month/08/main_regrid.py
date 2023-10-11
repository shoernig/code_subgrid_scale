import os, sys
from regrid_reff import DARDAR_L2toL3_regrid


ipath_dar = '/work/bb1093/b380620/DATA/Data/DARDAR_L2_cldclass_flag/'



#years = ['2007','2008','2009']
#years = ['2007','2008','2010','2009']
years = ['2008']

for year in years:
    ipath    = ipath_dar+year
    days     = os.listdir(ipath)
    for day in days:
        if day[5:7] == '08':
            print(day)
            DARDAR_L2toL3_regrid(year,day)
        

