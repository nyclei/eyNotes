#!/usr/bin/python
import sys
import subprocess
import time
import json
import requests
import os.path

#backupFile = '/Users/lile1/eyNotes/awsStageBackupSchemas.json'
#backupFile = '/Users/lile1/eyNotes/prodBackupSchemas.json'
backupFile = '/tmp/awsprod.id3.json'
restoreToBroker = "10.17.121.150:9092,10.17.125.215:9092,10.17.125.74:9092"     # <==== AwsProd
#restoreToBroker = "10.16.6.44:9092,10.16.4.53:9092, 10.16.5.11:9092"     # <===== AwsTest2
restoreToTopic = "_schemas2"


# ---------- editable above ---



if (not os.path.isfile(backupFile)):
    # From where to backup the _schema topic
    backupBroker = '10.17.125.74:9092'    # sys.argv[1]
    print 'Run following command for backup _schema from [backupBroker]:', backupBroker
    print "kafka-console-consumer --bootstrap-server [backupBroker] --topic _schemas --from-beginning  --property print.key=true --property key.separator=|  > [backupFile]"
    sys.exit(0)

with open (backupFile, "r") as myfile:
    for i, line in enumerate(myfile):
        #print i,'|',line
        line = line.strip()
        keyValueList = line.split("|", 2)
        if(len(keyValueList) < 2):
            continue

        k=keyValueList[0]
        v=keyValueList[1]

        if (v == 'null'):
            continue

        payload = json.loads(v)


        print
        print i
        print line
        deleted = payload.get('deleted')
        if(deleted is not True):
            # kafka-console-producer.sh  --broker-list 10.16.14.30:9092  --property "parse.key=true" --property "key.separator=|" --topic _schemas3
            p1 = subprocess.Popen(["echo", line], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p2 = subprocess.Popen(["kafka-console-producer",
                                    "--broker-list", restoreToBroker,
                                    "--property", "parse.key=true",
                                    "--property", "key.separator=|",
                                    "--topic", restoreToTopic], stdin=p1.stdout)
            p2.communicate()

            time.sleep(1)

            #raw_input('Send above data -> _schemas3? <ENTER>')

        #sys.exit(0)


#restoreBroker = 'localhost:9092'
#p1 = subprocess.Popen(["echo", line.strip()], stdout=subprocess.PIPE)
#p2 = subprocess.Popen(["kt", "produce", "-topic", kTopic, "-literal", "-brokers", restoreBroker], stdin=p1.stdout)
#p2.communicate()
