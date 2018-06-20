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
        sock.settimeout(10)
        if sock.connect_ex((host, port)) == 0:
            print " broker-", host,":",port,"is",bcolors.CYAN,"[Active]",bcolors.ENDC
        else:
            print " broker-",host,":",port,"is",bcolors.FAIL,"[Failed to Connect]",bcolors.ENDC

def check_kafka(env, publicNode, brokers):
    check_brokers(env, publicNode, brokers)
    check_rest_proxy(env, publicNode)
    check_schema_registry(env, publicNode)
    check_kafka_connect(env, publicNode)
#    check_docker_registry(env, publicNode)

def check_brokers(env, publicNode, brokers):
    print
    print bcolors.OKBLUE,env,bcolors.ENDC
    i = 0
    while i < len(brokers):
        check_socket(brokers[i], 9092)
        i += 1

def check_rest_proxy(env, publicSlaveNode):
    try:
    	code = urllib.urlopen("http://"+publicSlaveNode+":10132/topics").getcode()
    	if (code == 200):
            print "  Rest Proxy:  http://"+publicSlaveNode+":10132/topics ==>", bcolors.CYAN,str(code),bcolors.ENDC
    	else:
            print "  Rest Proxy:  http://"+publicSlaveNode+":10132/topics ==>", bcolors.FAIL,str(code),bcolors.ENDC
    except:
        print "  Rest Proxy:  http://"+publicSlaveNode+":10132/topics ==>", bcolors.FAIL,"Connection Refused",bcolors.ENDC


def check_schema_registry(env, publicSlaveNode):
    try:
        code = urllib.urlopen("http://"+publicSlaveNode+":10131/subjects").getcode()
        if (code == 200):
            print "  Schema Registry:  http://"+publicSlaveNode+":10131/subjects ==>", bcolors.CYAN,str(code),bcolors.ENDC
        else:
            print "  Schema Registry:  http://"+publicSlaveNode+":10131/subjects ==>", bcolors.FAIL,str(code),bcolors.ENDC
    except:
        print "  Schema Registry:  http://"+publicSlaveNode+":10131/subjects ==>", bcolors.FAIL,"Connection Refused",bcolors.ENDC

def check_kafka_connect(env, publicSlaveNode):
    try:
        code = urllib.urlopen("http://"+publicSlaveNode+":10109/connectors").getcode()
        if (code == 200):
            print "  Kafka Connect:  http://"+publicSlaveNode+":10109/connectors ==>", bcolors.CYAN,str(code),bcolors.ENDC
        else:
            print "  Kafka Connect:  http://"+publicSlaveNode+":10109/connectors ==>", bcolors.FAIL,str(code),bcolors.ENDC
    except:
        print "  Kafka Connect:  http://"+publicSlaveNode+":10109/connectors ==>", bcolors.FAIL,"Connection Refused",bcolors.ENDC

ssl._create_default_https_context = ssl._create_unverified_context
def check_docker_registry(env, publicSlaveNode):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        code = urllib.urlopen("https://"+publicSlaveNode+":10104/v2/_catalog", context=ctx).getcode()
        if (code == 200):
            print "  Kafka Connect:  https://"+publicSlaveNode+":10104/v2/_catalog ==>", bcolors.CYAN,str(code),bcolors.ENDC
        else:
            print "  Kafka Connect:  https://"+publicSlaveNode+":10104/v2/_catalog ==>", bcolors.FAIL,str(code),bcolors.ENDC
    except:
        print "  Kafka Connect:  https://"+publicSlaveNode+":10104/v2/_catalog ==>", bcolors.FAIL,"Connection Refused",bcolors.ENDC

def check_all():
    check_kafka("AWS Production", '10.17.121.235', ['10.17.125.74','10.17.121.27','10.17.122.121'])
    check_kafka("Ship - PR", "10.157.105.158", ['10.157.105.154','10.157.105.155','10.157.105.156'])
    check_kafka("Ship - MA", "10.132.105.158", ['10.132.105.154','10.132.105.155','10.132.105.156'])
    check_kafka("Ship - BR", "10.127.105.158", ['10.127.105.154','10.127.105.155','10.127.105.156'])
    #check_kafka("AWS Production", '10.17.121.235', ['10.17.125.74','10.17.121.27','10.17.122.121'])
    check_kafka("AWS Dev2 (new)", "10.16.4.176", ['10.16.7.7','10.16.6.71','10.16.4.39'])
    check_kafka("AWS Test2 (new)", "10.16.6.92", ['10.16.6.44','10.16.6.228','10.16.5.11'])
    check_kafka("AWS Staging", "10.17.131.92", ['10.17.135.9','10.17.132.82','10.17.131.176'])
    check_kafka("AWS Production", '10.17.121.235', ['10.17.125.74','10.17.121.27','10.17.122.121'])
    check_kafka("ShipTest", '10.135.105.158', ['10.135.105.154','10.135.105.155','10.135.105.156'])
    check_kafka("ShipTest2", "10.196.105.158", ['10.196.105.154','10.196.105.155','10.196.105.156'])
    check_kafka("Ship Staging", "10.137.105.158", ['10.137.105.154','10.137.105.155','10.137.105.156'])
    check_kafka("Ship - AL", "10.154.105.158", ['10.154.105.154','10.154.105.155','10.154.105.156'])
    check_kafka("Ship - SY", "10.165.105.158", ['10.165.105.154','10.165.105.155','10.165.105.156'])
    check_kafka("Ship - OA", "10.150.105.158", ['10.150.105.154','10.150.105.155','10.150.105.156'])
    check_kafka("Ship - SR", "10.130.105.158", ['10.130.105.154','10.130.105.155','10.130.105.156'])
    check_kafka("Ship - EN", "10.117.105.158", ['10.117.105.154','10.117.105.155','10.117.105.156'])
    check_kafka("Ship - AD", "10.126.105.158", ['10.126.105.154','10.126.105.155','10.126.105.156'])
    check_kafka("Ship - GR", "10.113.105.158", ['10.113.105.154','10.113.105.155','10.113.105.156']) 
    check_kafka("Ship - HM", "10.164.105.158", ['10.164.105.154','10.164.105.155','10.164.105.156'])
    check_kafka("Ship - EQ", "10.149.105.158", ['10.149.105.154','10.149.105.155','10.149.105.156'])
    check_kafka("AWS Sandbox", "10.16.6.61",  ['10.16.7.73','10.16.5.80','10.16.7.194','10.16.6.87','10.16.6.85'])
    check_kafka("Ship Sandbox", "10.196.105.198", ['10.196.105.194','10.196.105.195','10.196.105.196'])
    check_kafka("AWS Dev/Test", '10.16.4.8', ['10.16.7.199', '10.16.5.91','10.16.5.94','10.16.4.241'])

# TODO: refine later
if len(sys.argv) > 1:
    envCode = sys.argv[1]
    if(envCode == 'ShipSandbox'):
        check_kafka("Ship Sandbox", "10.196.105.198", ['10.196.105.194','10.196.105.195','10.196.105.196'])
    elif(envCode == 'MA'):
        check_kafka("Ship - MA", "10.132.105.158", ['10.132.105.154','10.132.105.155','10.132.105.156'])
    elif(envCode == 'BR'):
        check_kafka("Ship - BR", "10.127.105.158", ['10.127.105.154','10.127.105.155','10.127.105.156'])
    elif(envCode == 'prod'):
        check_kafka("AWS Production", '10.17.121.235', ['10.17.125.74','10.17.121.27','10.17.122.121'])
    elif(envCode == 'OA'):
        check_kafka("Ship - OA", "10.150.105.158", ['10.150.105.154','10.150.105.155','10.150.105.156'])
    elif(envCode == 'EQ'):
        check_kafka("Ship - EQ", "10.149.105.158", ['10.149.105.154','10.149.105.155','10.149.105.156'])
    elif(envCode == 'SS'):
        check_kafka("Ship - Sandbox", "10.196.105.198", ['10.196.105.194','10.196.105.195','10.196.105.196'])
    elif(envCode == 'ST1'):
        check_kafka("ShipTest", '10.135.105.158', ['10.135.105.154','10.135.105.155','10.135.105.156'])
    elif(envCode == 'ID'):
        check_kafka("Independence", '10.147.105.158', ['10.147.105.154','10.147.105.155','10.147.105.156'])
    elif(envCode == 'stag'):
        check_kafka("AWS Staging", "10.17.131.92", ['10.17.135.9','10.17.132.82','10.17.131.176'])


else:
    check_all()



