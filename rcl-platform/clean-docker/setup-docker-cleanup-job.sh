#!/bin/bash

if [ -z "$1" ]; then
    echo "Missing node ip4Addresses"
    echo "   Usage: ./setup-docker-cleanup-job.sh [nodeIp1] [nodeIp2] [nodeIp3] ..."
    exit 1
fi

for var in "$@"
do

  if [[ $var =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Setup new cron job to clean docker on node [$var]"
    scp ./new-crontab.txt $var:/tmp/new-crontab.txt
    scp ./append-cronjob.sh $var:/tmp/append-cronjob.sh
    ssh $var "chmod a+x /tmp/append-cronjob.sh"
    ssh -t $var "/tmp/append-cronjob.sh"
  else
    echo "Not an valid ip4Addr, skip [$var]."
  fi
done
