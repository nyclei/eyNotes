#!/usr/bin/python
import sys
import subprocess
import time
import json
import requests
import os.path

###############################################################################
# This tool needs to be copied to node which has following:
#     'kafka-console-consumer', for backup _schemas data
#     'python 2.7.x' with requests installed, for restoring
#
# I ran it from my localhost which has secured access to Cloud environments
# for backup with 'kafka-console-consumer' cmd. Later I can restore it to any
# environment by POSTing it to another environment's Schema Registry api
# endpoints:
# e.g. http://localhost:8081/subjects
#      http://10.196.105.158:10131/subjects
#
# Notes:
#   If the backup file is generated inside src-node docker container, you
#   need to copy it to the host and move it to the dest-node.
#   e.g. docker cp <containerId>:/file/path/within/container /host/path/target
#
# Other useful commands for testing:
# > kafka-topics --zookeeper localhost:2181 --topic _schemas --delete
# > kafka-topics --zookeeper localhost:2181 --topic _schemas --describe
###############################################################################

if (len(sys.argv) <= 1):
    print "Usage:"
    print "  ./restore.py [schema-registry-endpoint]"
    print "Example:  "
    print "  ./restore.py 'http://10.196.105.158:10131/subjects' \n"
    sys.exit(1)


# To where to restore the _schema topic
restoreSchemaRegistryBaseUrl = str(sys.argv[1])
#restoreSchemaRegistryBaseUrl = "http://localhost:8081/subjects"
#restoreSchemaRegistryBaseUrl = "http://10.196.105.158:10131/subjects"

kTopic  = "_schemas"
backupFile = '/tmp/tempSchemas.json'  # '/tmp/_schemas.backup.json'

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
        if (line == 'null'):
            continue
        payload = json.loads(line)
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

                payload.pop('id', None)
                payload.pop('version', None)
                payload.pop('subject', None)
                payload.pop('deleted', None)
                #print payload.keys()

                url = restoreSchemaRegistryBaseUrl+"/"+subject+"/versions"
                print "POST", url
                print json.dumps(payload)

                headers = { 'content-type':'application/json',
                            'Accept': "application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json"
                          }
                resp = requests.request("POST", url, data=json.dumps(payload), headers=headers)
                print "-->", resp.text
                time.sleep(1)
        except:
            continue



#restoreBroker = 'localhost:9092'
#p1 = subprocess.Popen(["echo", line.strip()], stdout=subprocess.PIPE)
#p2 = subprocess.Popen(["kt", "produce", "-topic", kTopic, "-literal", "-brokers", restoreBroker], stdin=p1.stdout)
#p2.communicate()
