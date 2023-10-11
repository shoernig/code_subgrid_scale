#!/bin/bash
#SBATCH --account=bb1093
#SBATCH --job-name=07_L2regrid     # Specify job name
#SBATCH --partition=compute        # Use partition prepost
#SBATCH --nodes=1                  # Specify max. number of tasks to be invoked
#SBATCH --mem-per-cpu=5300         # Set memory required per allocated CPU
#SBATCH --time=08:00:00            # Set a limit on the total run time
#SBATCH --output=log_L2toL3.out    # File name for standard and error output

python main_regrid.py

