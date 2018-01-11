#!/bin/bash
##
## Time-stamp: <2016-08-05 11:11:17 (cluettig)>
##  


fdir=$1
echo $fdir
cd segments_filter
./filter.gmt $fdir
cd ../median_filter
./filter.gmt all $fdir f f1
cd ../directional_filter
./filter.gmt all $fdir f mf_f1
cd ..
