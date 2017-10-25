#!/bin/bash
##
## Time-stamp: <2016-08-05 11:11:17 (cluettig)>
## 
#for ((i=2;i<=50;i+=2)); 
#do 
#    #p=$(grep "^minimum" parameter.txt |awk -F : '{print $2}')
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    sed -i '/^minimum/d' parameter.txt
#    sed -i "8iminimum number of elements in a segment:$i" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    ./run_filter.sh
#    cat -A -n parameter.txt
#    sleep 2
#done
#sed -i '/^minimum/d' parameter.txt
#sed -i "8iminimum number of elements in a segment:8" parameter.txt
p=0.0
for ((i=1;i<=10;i+=1)); 
do 
    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
    id=$(echo "$id + 1" | bc)
    p=$(echo "$p +0.1" | bc)
    sed -i '/^a:/d' parameter.txt
    sed -i "8ia:$p" parameter.txt
    sed -i 's/id.*$/id :'$id'/' parameter.txt
    cat -A -n parameter.txt
    ./run_filter.sh
    sleep 2
done
sed -i '/^a/d' parameter.txt
sed -i "9ia:0.2" parameter.txt
#p=0.9
#for ((i=1;i<=11;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +0.1" | bc)
#    sed -i '/^difference/d' parameter.txt
#    sed -i "9idifference to prior field factor:$p" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    cat -A -n parameter.txt
#    ./run_filter.sh
#    sleep 2
#done
#sed -i '/^difference/d' parameter.txt
#sed -i "9idifference to prior field factor:1.5" parameter.txt
#p=0.5
#for ((i=1;i<=9;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +0.5" | bc)
#    sed -i '/^eps std/d' parameter.txt
#    sed -i "26ieps std:$p" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    cat -A -n parameter.txt
#    ./run_filter.sh
#    sleep 2
#done
#sed -i '/^eps std/d' parameter.txt
#sed -i "26ieps std:3" parameter.txt
#p=0.5
#for ((i=1;i<=9;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +0.5" | bc)
#    sed -i '/^e std/d' parameter.txt
#    sed -i '$ae std:'$p'' parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    ./run_filter.sh
#    cat -A -n parameter.txt
#    sleep 2
#done
#sed -i '/^e std/d' parameter.txt
#sed -i '$ae std:3' parameter.txt
#p=0
#for ((i=1;i<=9;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +5" | bc)
#    sed -i '/^chipsize median/d' parameter.txt
#    sed -i "25ichipsize median:$p" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    ./run_filter.sh
#    cat -A -n parameter.txt
#    sleep 2
#done
#sed -i '/^chipsize median/d' parameter.txt
#sed -i "25ichipsize median:25" parameter.txt
#p=0
#for ((i=1;i<=9;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +5" | bc)
#    sed -i '/^chipsize direction/d' parameter.txt
#    sed -i "30ichipsize direction:$p" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    cat -A -n parameter.txt
#    ./run_filter.sh
#    sleep 2
#done
#sed -i '/^chipsize direction/d' parameter.txt
#sed -i "30ichipsize direction:25" parameter.txt
#p=0
#for ((i=1;i<=12;i+=1)); 
#do 
#    id=$(grep "^id" parameter.txt |awk -F : '{print $2}')
#    id=$(echo "$id + 1" | bc)
#    p=$(echo "$p +2.5" | bc)
#    sed -i '/^angle/d' parameter.txt
#    sed -i "29iangle:$p" parameter.txt
#    sed -i 's/id.*$/id :'$id'/' parameter.txt
#    cat -A -n parameter.txt
#    ./run_filter.sh
#    sleep 2
#done
#sed -i '/^angle/d' parameter.txt
#sed -i "29iangle:20" parameter.txt
