#!/usr/bin/python
import sys
import subprocess
import time
import json
import requests
import os.path



backupFile = '/tmp/prodBackupSchemas.json'

if (not os.path.isfile(backupFile)):
    # From where to backup the _schema topic
    backupBroker = '10.17.125.74:9092'    # sys.argv[1]
    print 'Run following command for backup _schema from Broker:', backupBroker
    print '> kafka-console-consumer --bootstrap-server '+backupBroker+' --topic _schemas --from-beginning > ' + backupFile
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
        try:
            print
            print i
            #print line
            deleted = payload.get('deleted')
            if(deleted is not True):
                subject = payload.get('subject').strip("', /\n[]{}()<>*")
                version = payload.get('version')

                #print 'subject', ':', subject    # "string"
                #print 'version', ':', version    # int
                #print 'id', ':', payload.get('id')              # int
                #print 'deleted', ':', deleted    # true or false
                #print payload.keys()

                #payload.pop('id', None)
                #payload.pop('version', None)
                #payload.pop('subject', None)
                payload.pop('deleted', None)
                #payload.pop('schema', None)
                #print payload.keys()

                message = json.dumps(payload)

                newMsgTemplate= {"key": k, "value": message, "partition": 0}
                print "key=", k
                print "value=", message
                print "WholeMsg=", json.dumps(newMsgTemplate)
                p1 = subprocess.Popen(["echo", json.dumps(newMsgTemplate)], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(["kt", "produce", "-topic", "_schemas3", "-literal", "-brokers", "10.16.14.30:9092,10.16.14.7:9092,10.16.14.17:9092"], stdin=p1.stdout)
                p2.communicate()
                #time.sleep(1)

        except:
            print 'Failed'
            continue

        raw_input('Send above data -> _schemas3? <ENTER>')
        sys.exit(1)


#restoreBroker = 'localhost:9092'
#p1 = subprocess.Popen(["echo", line.strip()], stdout=subprocess.PIPE)
#p2 = subprocess.Popen(["kt", "produce", "-topic", kTopic, "-literal", "-brokers", restoreBroker], stdin=p1.stdout)
#p2.communicate()
