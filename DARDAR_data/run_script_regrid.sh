#!/bin/bash

path=$(pwd)

echo $path




for mon in 01 02 03 04 05 06 07 08 09 10 11 12
do
cd $path/month/$mon
pwd
cp $path/scripts/regrid.py . # copy regrid.py file to all month directories
cp $path/scripts/regrid_reff.py .
#ls -lrth
rm -f main_regrid.py #run_regrid.sh

cat>>main_regrid.py<<EOF
import os, sys
from regrid import DARDAR_L2toL3_regrid


ipath_dar = '/work/bb1093/b380620/DATA/Data/DARDAR_L2_cldclass_flag/'



#years = ['2007','2008','2009']
#years = ['2007','2008','2010','2009']
years = ['2008']

for year in years:
    ipath    = ipath_dar+year
    days     = os.listdir(ipath)
    for day in days:
        if day[5:7] == '$mon':
            print(day)
            DARDAR_L2toL3_regrid(year,day)
        

EOF

rm run_regrid.sh

cat >>run_regrid.sh<<EOF
#!/bin/bash
#SBATCH --account=bb1093
#SBATCH --job-name=${mon}_L2regrid     # Specify job name
#SBATCH --partition=compute        # Use partition prepost
#SBATCH --nodes=1                  # Specify max. number of tasks to be invoked
#SBATCH --mem-per-cpu=5300         # Set memory required per allocated CPU
#SBATCH --time=08:00:00            # Set a limit on the total run time
#SBATCH --output=log_L2toL3.out    # File name for standard and error output

python main_regrid.py

EOF


chmod u+x run_regrid.sh



# ls

sbatch run_regrid.sh

done
