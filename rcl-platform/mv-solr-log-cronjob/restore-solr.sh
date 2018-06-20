#!/bin/bash

# Running as 'mesossu' since the log is stored under mesossu folder
if [ $(whoami) != "mesossu" ]; then
    echo "This job needs to be run as 'mesossu'."
    exit 1
fi

if [ -z "$1" ]; then
    echo "Missing filename of solr tgz"
    echo "   Usage: ./restore-solr.sh 'solr.2018-05-14-07-30-44.tgz' "
    exit 1
fi

sourceTgzFileName=$1

# uncompress selected tgz
cd /tmp
mkdir -p /tmp/solr-restore
cd /tmp/solr-restore
tar xvf /mnt/nfs/solr_backups/$sourceTgzFileName
cd /tmp/solr-restore/data/commerce/solr-data/multiship/6.4.2-7-95154f/
mv commerce_products_index_shard1_replica2 commerce_products_index_shard1_replica1 2>/dev/null

# backup existing 6.6.0-0-restore
cd /data/commerce/solr-data/interport
NOW=`date +%Y-%m-%d-%H-%M-%S`
sudo mv "6.6.0-0-restore" "6.6.0-0-restore.backup.$NOW"  2>/dev/null

# move data
sudo mv /tmp/solr-restore/data/commerce/solr-data/multiship/6.4.2-7-95154f /data/commerce/solr-data/interport/6.6.0-0-restore
sudo chown -R root:root /data/commerce/solr-data/interport/6.6.0-0-restore


# remove the leftover
rm -rf /tmp/solr-restore
