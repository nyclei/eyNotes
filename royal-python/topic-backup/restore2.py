#!/usr/bin/python
import sys
import subprocess
import time

start = 0
jsonFile = '/tmp/tempSchemas.json'
kTopic  = "_schemas"
kServer = "10.16.14.30:9092,10.16.14.7:9092,10.16.14.17:9092"
tempfile = '/tmp/temporaryHuge.json.tmp'

with open (jsonFile, "r") as myfile:
    for i, line in enumerate(myfile):
        lineLength = len(line)
        print '>>---' + str(i) + '-- length=' + str(lineLength)
        if i >= start:
            print line
            #print str(i) + '-- length=' + str(lineLength) + ' ---<<'

            line = line.encode('string-escape')
            print line

            if(lineLength > 256000):
                with open(tempfile, "w") as text_file:
                    text_file.write(line)
                text_file.close()
                p1 = subprocess.Popen(["cat", tempfile], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(["kt", "produce", "-topic", kTopic, "-literal", "-brokers", kServer], stdin=p1.stdout)
                p2.communicate()
            else:
                p1 = subprocess.Popen(["echo", line], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(["kt", "produce", "-topic", kTopic, "-literal", "-brokers", kServer], stdin=p1.stdout)
                p2.communicate()


            raw_input('Send above data -> _schemas? <ENTER>')
