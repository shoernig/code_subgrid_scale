#!/bin/bash
#SBATCH -J DAR_10              # Specify job name
#SBATCH -p compute             # Use partition prepost
#SBATCH -N 1                   # Specify number of nodes
#SBATCH -n 1                   # Specify max. number of tasks to be invoked
#SBATCH --mem-per-cpu=5300     # Set memory required per allocated CPU
#SBATCH -t 08:00:00            # Set a limit on the total run time
#SBATCH -A bb1093              # Charge resources on this project account
# #SBATCH -o log.out          # File name for standard and error output

python main.py
