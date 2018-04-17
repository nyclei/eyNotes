#!/bin/bash

DOCKER_CLEANUP_CRONJOB_EXIST=$(sudo crontab -l | grep 'docker rm')
if [ -z "$DOCKER_CLEANUP_CRONJOB_EXIST" ]; then
  sudo crontab -l | cat - /tmp/new-crontab.txt  > /tmp/all-crontab.txt && sudo crontab /tmp/all-crontab.txt
  sudo rm /tmp/all-crontab.txt
fi
