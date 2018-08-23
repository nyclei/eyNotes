#!/usr/bin/python

import socket
#import numpy
from contextlib import closing
import urllib
import ssl
import sys
import errno
from socket import error as socket_error
import requests
import csv
from sets import Set
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    CYAN = '\033[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_kafka_connect_ncp(host, port):
    destUrl = "http://"+host+":"+port+"/connectors"
    print "  -> curl " + destUrl
    try:
        code = urllib.urlopen(destUrl).getcode()
        if (code == 200):
            print "  Kafka Connect:  "+destUrl+" ==>", bcolors.CYAN,str(code),bcolors.ENDC
        else:
            print "  Kafka Connect:  "+destUrl+" ==>", bcolors.FAIL,str(code),bcolors.ENDC
    except:
        print "  Kafka Connect:  "+destUrl+" ==>", bcolors.FAIL,"Connection Refused",bcolors.ENDC

def check_connect_by_str(connectStr):
    ary = connectStr.split("_")
    host = ary[0]+"."+ary[1]+"."+ary[2]+"."+ary[3]
    port = ary[4]
    check_kafka_connect_ncp( host, port)

def parse_mlb_csv(pub_node):
    testfile = urllib.URLopener()
    tempFile = "/tmp/"+pub_node+".csv"
    testfile.retrieve('http://'+pub_node+':9090/haproxy?stats;csv', tempFile)

    mySet = Set([])
    with open(tempFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if (row[0] == "confluent_connect_10109" and row[1] != 'FRONTEND' and row[1] != 'BACKEND'):
                # print(row[0] +",  "+row[1])
                # check_connect_by_str(row[1])
                mySet.add(row[1])
    os.remove(tempFile)
    for u in mySet:
        check_connect_by_str(u)


def main(argv):
    if len(sys.argv) == 1:
        print "Usage:  python checkConnectors.py pubNodeIP"
        print "Example:   /tmp/checkConnectors.py 10.154.105.158  "
        sys.exit()
    parse_mlb_csv(sys.argv[1])

if __name__ == "__main__":
    main(sys.argv)
