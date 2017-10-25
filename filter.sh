#!/bin/bash
##
## Time-stamp: <2016-08-05 11:11:17 (cluettig)>
##    
#SBATCH --job-name=filter
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --mail-user=cluettig@awi.de
#SBATCH --mail-type=END

ulimit -s unlimited
module purge
module load gcc
module load GMT
module load python
module load gdal

fdir=$1
echo $fdir
cd segments_filter
srun ./filter.gmt $fdir
cd ../median_filter
srun ./filter.gmt all $fdir f f1
cd ../directional_filter
srun ./filter.gmt all $fdir f mf_f1
cd ..


