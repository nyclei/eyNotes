#!/bin/bash

if [ -z "$1" ]; then
    echo "Missing docker registry node ip"
    echo "   Usage: ./janitor-clean-ip.sh [dockerRegistryNodeIP]"
    exit 1
fi 

scp janitor-clean.noRun $1:/tmp/janitor-clean.noRun
ssh -t $1 "bash /tmp/janitor-clean.noRun"
ssh $1 "rm /tmp/janitor-clean.noRun"

