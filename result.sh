#!/bin/bash
if (( $# < 1 )) 
then
 printf "Enter USN number\n";
 read USN;
elif (( $# > 1 ))
then
 printf "Bad usage\n./results.sh USN\n";
else
 USN="$1"
fi
let i=0
while [[ -z "${res//}" ]] 
do
 ((i++)) 
 echo "try $i"
 res=$(curl -sd "USN=$USN&submit_result=Fetch+Result" http://sjce.ac.in/view-results | grep -zoE "(<tr>.*</tr>|<center>.*</center>)"| sed -e 's/<[^>]*>//g' | tr -d '\0'| tr ':' '-' |tr -s '\n' | sed '/^\s*$/d' | sed  '/Name/a\\' | paste -sd '::\n' | cut -d':' -f1,3)
echo $res
#sleep 1
done
