#!/usr/bin/python

import socket
#import numpy
from contextlib import closing

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

# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# result = sock.connect_ex(('127.0.0.1',80))
# if result == 0:
#    print "Port is open"
# else:
#    print "Port is not open"


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(5)
        if sock.connect_ex((host, port)) == 0:
            print " broker-", host,":",port,"is",bcolors.CYAN,"[Active]",bcolors.ENDC
        else:
            print " broker-",host,":",port,"is",bcolors.FAIL,"[Failed to Connect]",bcolors.ENDC

def check_kafka(env, brokers):
    print
    print bcolors.OKBLUE,env,bcolors.ENDC
    i = 0
    while i < len(brokers):
        check_socket(brokers[i], 9092)
        i += 1

check_kafka("AWS Dev/Test", ['10.16.7.199','10.16.5.91','10.16.5.94'])
check_kafka("AWS Test (new)", ['10.16.6.44','10.16.6.228','10.16.4.189'])
check_kafka("AWS Staging", ['10.17.135.9','10.17.132.82','10.17.131.176'])
check_kafka("AWS Production", ['10.17.125.74','10.17.121.27','10.17.122.121'])
check_kafka("ShipTest", ['10.135.105.154','10.135.105.155','10.135.105.156'])
check_kafka("ShipTest2", ['10.196.105.154','10.196.105.155','10.196.105.156'])
check_kafka("Ship Staging", ['10.137.105.154','10.137.105.155','10.137.105.156'])
check_kafka("Ship - AL", ['10.154.105.154','10.154.105.155','10.154.105.156'])
check_kafka("Ship - SY", ['10.165.105.154','10.165.105.155','10.165.105.156'])
check_kafka("Ship - OA", ['10.150.105.154','10.150.105.155','10.150.105.156'])
check_kafka("Ship - SR", ['10.130.105.154','10.130.105.155','10.130.105.156'])
check_kafka("Ship - EN", ['10.117.105.154','10.117.105.155','10.117.105.156'])
check_kafka("Ship - AD", ['10.126.105.155','10.126.105.155','10.126.105.156'])

check_kafka("AWS Sandbox", ['10.16.7.73','10.16.5.80','10.16.7.194','10.16.6.87','10.16.6.85'])