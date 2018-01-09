#!/bin/bash

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n100 -c1 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n100-c1.txt
sleep 1
cat n100-c1.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n200 -c2 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n200-c2.txt
sleep 1
cat n200-c2.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n300 -c3 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n300-c3.txt
sleep 1
cat n300-c3.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n400 -c4 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n400-c4.txt
sleep 1
cat n400-c4.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n500 -c5 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n500-c5.txt
sleep 1
cat n500-c5.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2

cat fd-urls.txt |parallel --citation "ab -l -s 100 -q -n600 -c6 {} | grep 'Requests per second' | sed -e 's/.* \([0-9][^ ]*\) .*/\1/' 2>&1 " > n600-c6.txt
sleep 1
cat n600-c6.txt |  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ +/g' | bc
sleep 2
