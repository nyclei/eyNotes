#!/usr/bin/bash

containerPath=$(dcos marathon app show '/shared-services/registry' | jq -r '.container.volumes[] | select(.mode == "RW") | .hostPath ')

subPath="/docker/registry/v2"

regDataPath="$containerPath$subPath"

if [ -d "$regDataPath" ]; then
  REGISTRY_DATA_DIR="$regDataPath"; export REGISTRY_DATA_DIR
  echo "export REGISTRY_DATA_DIR=$REGISTRY_DATA_DIR"
else
  echo "Error: invalid path: [$regDataPath]"
fi
