#!/bin/bash

# Usage: ./backup.sh 10.17.125.74:9092 /tmp/ttttttt.json
#        ./backup.sh 10.17.125.74:9092 /tmp/prodBackupSchemas.json


# awsprod: 10.17.125.74:9092
# awsStage: 10.17.132.82:9092,10.17.135.9:9092
# shipStage: 	10.137.105.154:9092
backupBroker=$1
backupFile=$2
echo "kafka-console-consumer --bootstrap-server $backupBroker --topic _schemas --from-beginning  --property \"print.key=true\" --property \"key.separator=|\"  > $backupFile"
kafka-console-consumer --bootstrap-server $backupBroker --topic _schemas --from-beginning  --property "print.key=true" --property "key.separator=|"  > $backupFile
