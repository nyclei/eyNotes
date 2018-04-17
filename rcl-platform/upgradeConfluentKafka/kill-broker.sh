#!/bin/bash
if [ -z "$1" ]; then
    echo "Missing broker node ip"
    echo "   Usage: ./kill-brokers.sh [brokerAgentNodeIP]"
    exit 1
fi 

scp kill-broker.noRun $1:/tmp/kill-broker.noRun
ssh -t $1 "sudo bash /tmp/kill-broker.noRun"
ssh $1 "rm /tmp/kill-broker.noRun"

