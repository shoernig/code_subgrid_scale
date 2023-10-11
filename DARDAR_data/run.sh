#!/bin/bash

path=$(pwd)

echo $path




for mon in 01 02 03 04 05 06 07 08 09 10 11 12
do
cd $path/month/$mon
pwd

cp $path/scripts/cldclass.py .
cp $path/scripts/cldclass_combprec.py .
cp $path/scripts/cldclass_reff.py .

rm -f main.py #run.sh

cat >>main.py<<EOF
import os, sys
from cldclass_reff import DARDAR_cldclass


ipath = '/work/bb1093/b380620/DATA/Data/2B-CLDCLASS/'
ipathDAR = '/scratch/b/b380333/share/DARDAR-Nice/DARNI_L2_PRO.v2.0/'
years = os.listdir(ipath)

year = '2009'

ipath    = ipath+year
ipathDAR = ipathDAR+year
days     = os.listdir(ipath)
daysDAR  = os.listdir(ipathDAR)




for day in days:
    if day[5:7] == '$mon':
        print(day)
        
        if day in daysDAR:  
            DARDAR_cldclass(year,day)
            
EOF





rm -f run.sh
cat >>run.sh<<EOF
#!/bin/bash
#SBATCH -J DAR_$mon              # Specify job name
#SBATCH -p compute             # Use partition prepost
#SBATCH -N 1                   # Specify number of nodes
#SBATCH -n 1                   # Specify max. number of tasks to be invoked
#SBATCH --mem-per-cpu=5300     # Set memory required per allocated CPU
#SBATCH -t 08:00:00            # Set a limit on the total run time
#SBATCH -A bb1093              # Charge resources on this project account
# #SBATCH -o log.out          # File name for standard and error output

python main.py
EOF

chmod u+x run.sh

ls

sbatch run.sh

done
