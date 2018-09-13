#!/bin/bash

set -e
registry="stg-registry.nowlab.tstsh.tstrccl.com:10104"

repos=`curl https://$registry/v2/_catalog?n=2000 | jq '.repositories[]' | tr -d '"'`

for repo in $repos; do
   tags=`curl -s https://$registry/v2/$repo/tags/list | jq '.tags[]' | tr -d '"'`
   for tag in $tags; do
      echo "delete_docker_registry_image --image $repo:$tag --dry-run"
   done
done
