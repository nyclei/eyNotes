#!/bin/bash

Usage()
{
    echo " Prerequisites: "
    echo "      - 'brew install parallel' if parallel is missing "
    echo "      - 'fd-urls.txt' exists with some absolute urls"
    echo "  Example:"
    echo "    ./testNTimes.sh 8"
}

startAb()
{
    N=$((50*$C))
    FN="n$N""_""c$C.txt"
    cat fd-urls.txt |parallel "ab -l -s 100 -q -n$N -c$C {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > $FN
    sleep 1
    printf "$FN - "
    cat $FN |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | awk '{print "scale=2; ("$1 $2") / 2" }' | bc
    sleep 1
}

# basic validation
if [ -z "$1" ];
then
    echo
    echo "!! Error: missing argument. !!"
    echo
    Usage
    echo
    exit 0
fi

# enter startAb loop
C=1
while [  $C -le $1 ]; do
    startAb
    (( C++ ))
done
