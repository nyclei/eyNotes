#!/bin/bash

if [ -z "$1" ]; then
    echo "Missing node ipAddr"
    echo "   Usage: ./uploadAndInstall.sh [nodeIp1] [nodeIp2] [nodeIp3] ..."
    exit 1
fi

for var in "$@"
do
  if [[ $var =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "upload 3 certs to node [$var]"
    scp ./GlobalSignCloudSSLCA-SHA256-G3.crt $var:/tmp/GlobalSignCloudSSLCA-SHA256-G3.crt
    scp ./GlobalSignRootCA.crt               $var:/tmp/GlobalSignRootCA.crt
    scp ./f2sharedglobalfastlynet.crt        $var:/tmp/f2sharedglobalfastlynet.crt

    echo "upload installLaunchDarklyCerts script to node [$var]"
    scp ./installLaunchDarklyCerts.noRun     $var:/tmp/installLaunchDarklyCerts.sh

    ssh -q $var "chmod a+x /tmp/installLaunchDarklyCerts.sh"
    ssh -q -t $var "sudo /tmp/installLaunchDarklyCerts.sh"
    ssh -q $var "chmod a-x /tmp/installLaunchDarklyCerts.sh" # Keep it for debugging,
    # ssh -q $var "rm /tmp/installLaunchDarklyCerts.sh"
  else
    echo "Not an valid ip4Addr, skip [$var]."
  fi
done
