#!/bin/bash

backupBroker=$1
backupFile=$2
kafka-console-consumer --bootstrap-server $backupBroker --topic _schemas --from-beginning > $backupFile
