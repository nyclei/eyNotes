#!/bin/bash

# separate this script from main solr collection moving script.
# change ownership of log files per PCP team request

TODAY=`date +%Y-%m-%d`
NOWTIME=`date +%H:%M:%S`

echo "$TODAY : $NOWTIME : start changing owner and moving logs"

sudo find /home/mesossu/prod-solr-log -type f -name "*.tgz" -exec mv {} /home/mesosadm/prod-solr-log \;
sudo chown -R  mesosadm:mesosadm /home/mesosadm/prod-solr-log
sudo find /home/mesosadm/prod-solr-log  -type f -mtime +2 -name "*.tgz" -print -exec rm {} \;

echo "$TODAY : $NOWTIME : Moved all solr log files(.tgz) on $DEST_SERVER from /home/mesossu to /home/mesosadm... DONE!"
