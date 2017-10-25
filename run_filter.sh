#!/bin/bash
##
## Time-stamp: <2016-08-05 11:11:17 (cluettig)>
##
vx=$(grep "^vx" parameter.txt |awk -F : '{print $2}')
vy=$(grep "^vy" parameter.txt |awk -F : '{print $2}')
id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#id=$(echo "$id + 1" | bc)
echo $vx
echo $vy

path=$(dirname $vx)
bx=$(basename $vx)
by=$(basename $vy)
end=${bx/*./}
fdir=$path/filter_$id
echo "All data will be saved in directory" $fdir
#sed -i 's/id.*$/id :'$id'/' parameter.txt
mkdir $fdir
newx=$fdir/vx.nc
newy=$fdir/vy.nc
cp parameter.txt $fdir/parameter.txt

if [ $end == 'tif' ]; then
    gdal_translate -of NetCDF $vx $newx
    gdal_translate -of NetCDF $vy $newy
elif [ $end == 'nc' ]; then
    cp $vx $newx
    cp $vy $newy
else
    echo "Unknown file format" $end ". Try NetCDF or GeoTIFF."
fi
vx=$newx
vy=$newy

unit=$(grep "^unit" $fdir/parameter.txt |awk -F : '{print $2}')
if [ $unit == "m/d" ]; then

    gmt grdmath $vx 365.25 MUL = $vx
    gmt grdmath $vy 365.25 MUL = $vy
fi
sbatch filter.sh $fdir
