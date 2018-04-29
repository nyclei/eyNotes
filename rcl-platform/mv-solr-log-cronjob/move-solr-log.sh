#!/bin/bash

# Running as 'mesossu' since the log is stored under mesossu folder
if [ $(whoami) != "mesossu" ]; then
    echo "This job needs to be run as 'mesossu'."
    exit 1
fi

TODAY=`date +%Y-%m-%d`
echo "*************** $TODAY ***************"
mkdir -p "/tmp/$TODAY"
SRC="10.17.121.27"
DEST_SERVER="10.16.4.101"
DEST_PATH="/home/mesossu/prod-solr-log"

ssh $DEST_SERVER "rm -rf $DEST_PATH"
ssh $DEST_SERVER "mkdir -p $DEST_PATH"

mx=50
FILES=$(ssh -q $SRC "find . -type f -maxdepth 2  -mtime -1 -name '*.tgz' | sort")
for f in $FILES; do
    NOWTIME=`date +%H:%M:%S`
    echo "$TODAY : [$NOWTIME] copy - $f"
    # copy it down
    scp "10.17.121.27:$f" "/tmp/$TODAY"
    sleep 1

    # copy it to another machine
    scp "/tmp/$TODAY/$f"  "$DEST_SERVER:$DEST_PATH"
    sleep 1

    # remove it locally
    rm "/tmp/$TODAY/$f"
    echo "       [$f] is copied to $DEST_SERVER:$DEST_PATH"

    let "mx=mx-1"
    if (( $mx==0 )); then
        break
    fi
done

rm -rf "/tmp/$TODAY"
echo "Remove temporary folder /tmp/$TODAY folder"

