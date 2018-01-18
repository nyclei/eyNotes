#!/bin/bash
COUNTER=$1
REST=400
while [  $COUNTER -lt 45000 ]; do
    if [ $REST == 0 ];
    then
        let REST=400
        sleep 10s
        continue
    else
        echo "curl -k -s https://dev3.nj01/test/data/cache_content.jsp?sku=$COUNTER&version="
        curl -k -s "https://dev3.nj01/test/data/cache_content.jsp?sku=$COUNTER&version="  > /dev/null &
        let COUNTER=COUNTER+1
        let REST=REST-1
    fi
done
