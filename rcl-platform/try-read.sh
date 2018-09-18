#!/bin/bash

echo
read -r -p "Broker CPUs [0.2~12~12] (unit): " BROKER_CPUS
BROKER_CPUS=${BROKER_CPUS:-12}
echo "BROKER_CPUS=$BROKER_CPUS"

read -r -p "Broker Memory [2~65536~65536] (M): " BROKER_MEM
BROKER_MEM=${BROKER_MEM:-65536}
echo "BROKER_MEM=$BROKER_MEM"

read -r -p "Broker Disk [20000~460800~2900000] (M): " BROKER_DISK
BROKER_DISK=${BROKER_DISK:-460800}
echo "BROKER_DISK=$BROKER_DISK"