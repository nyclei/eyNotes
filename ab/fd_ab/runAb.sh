#!/bin/bash

URL=$1

echo '-----------------------------------------------'
echo "URL: $URL "
echo "Req count: $numOfReqs "
echo '-----------------------------------------'
echo "[Currency#, RPS1, RPS2, RPS3]"
echo '-----------------------------------------'

for((c=3;c<=81;c+=3)); do
  read numOfReqs <<< $(echo "$c*50" | bc)
  read rps1 <<< $(ab -l -s 100 -q -n$numOfReqs -c$c $URL | grep 'Requests per second' | awk '/Requests/ {print $4}' | bc)
  #echo "   [$c,    $rps1]"

  read rps2 <<< $(ab -l -s 100 -q -n$numOfReqs -c$c $URL | grep 'Requests per second' | awk '/Requests/ {print $4}' | bc)
  read rps3 <<< $(ab -l -s 100 -q -n$numOfReqs -c$c $URL | grep 'Requests per second' | awk '/Requests/ {print $4}' | bc)
  #read rps <<< $(echo "scale=2; ($rps1+$rps2+$rps3)/3" | bc)
  #echo "   $c           $rps"
  echo "   [$c, $rps1, $rps2, $rps3 ],"
  sleep 1  # Take a break
done
