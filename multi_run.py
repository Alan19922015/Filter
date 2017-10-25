import os
import fnmatch
import numpy as np


inpath = "/work/ollie/nneckel/GRE/S1_offset_tracking_GRE/Greenland/geotifs/masked_vel/"
outpath = "/work/ollie/cluettig/filter_fertig/multi_run/" 
step=100

def slice_per(source, step):
    return [source[i::step] for i in range(step)]

name_list=[]
for file in os.listdir(inpath):
	if fnmatch.fnmatch(file, '*mag_masked.tif'):
		name = file[:-15]
		name_list = np.append(name_list,name)

sliced_list = slice_per(name_list,step)

for i in np.arange(len(sliced_list)):
	jobfile = open("job_"+str(i)+".slr","w")
	jobfile.write("#!/bin/bash\n")
	jobfile.write("#SBATCH --job-name=flt_"+str(i)+"\n")
	jobfile.write("#SBATCH -c 8 \n")
	jobfile.write("#SBATCH --time=12:00:00\n")
	jobfile.write("ulimit -s unlimited\n")
	jobfile.write("module load gcc\n")
	jobfile.write("module load python\n")
	jobfile.write("module load gdal\n")
	jobfile.write("module load GMT\n")	
	for j in np.arange(len(sliced_list[i])):
		vx = inpath+sliced_list[i][j]+"_east_masked.tif"
		vy = inpath+sliced_list[i][j]+"_north_masked.tif"
		jobfile.write("gdal_translate -of NetCDF "+vx+" "+outpath+sliced_list[i][j]+"_east_masked.nc\n")
		jobfile.write("gdal_translate -of NetCDF "+vy+" "+outpath+sliced_list[i][j]+"_north_masked.nc\n")
		vx = outpath+sliced_list[i][j]+"_east_masked.nc"
		vy = outpath+sliced_list[i][j]+"_north_masked.nc"
		jobfile.write("gmt grdmath "+vx+" 365.25 MUL = "+vx+"\n")
		jobfile.write("gmt grdmath "+vy+" 365.25 MUL = "+vy+"\n")
		jobfile.write("cd "+outpath+"Rosenaufilter\n")
		jobfile.write("srun ./filter.gmt "+vx+" "+vy+"\n")
		vx = outpath+sliced_list[i][j]+"_east_masked_flt.nc"
		vy = outpath+sliced_list[i][j]+"_north_masked_flt.nc"
		jobfile.write("cd ../Medianfilter\n")
		jobfile.write("srun ./filter.gmt "+vx+" "+vy+"\n")
		jobfile.write("cd ../Richtungsfilter\n")
		jobfile.write("srun ./filter.gmt "+vx+" "+vy+"\n")
		jobfile.write("gmt grdmath "+vx+" 365.25 DIV = "+vx+"\n")
		jobfile.write("gmt grdmath "+vy+" 365.25 DIV = "+vy+"\n")
		jobfile.write("gdal_translate "+vx+" "+outpath+sliced_list[i][j]+"_east_masked_flt.tif\n")
		jobfile.write("gdal_translate "+vy+" "+outpath+sliced_list[i][j]+"_north_masked_flt.tif\n")
	
	jobfile.close()
	os.system("chmod 775 "+outpath+"job_"+str(i)+".slr")
	#os.system("cd "+outpath+" ; sbatch job_file"+str(i)+".slr")
