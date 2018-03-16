import socket
import numpy
from contextlib import closing

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
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
            print " broker-", host,":",port," is [Active]"
        else:
            print " broker-",host,":",port," is",bcolors.FAIL,"[Failed to Connect]",bcolors.ENDC

def check_kafka(env, brokers):
    print env
    check_socket(brokers[0], 9092)
    check_socket(brokers[1], 9092)
    check_socket(brokers[2], 9092)

check_kafka("AWS Dev/Test", ['10.16.7.199','10.16.5.91','10.16.5.94'])
check_kafka("AWS Staging", ['10.17.135.9','10.17.132.82','10.17.131.176'])
check_kafka("AWS Production", ['10.17.125.74','10.17.121.27','10.17.122.121'])
check_kafka("ShipTest", ['10.135.105.154','10.135.105.155','10.135.105.156'])
check_kafka("Ship Staging", ['10.137.105.154','10.137.105.155','10.137.105.156'])
check_kafka("Ship - AL", ['10.154.105.154','10.154.105.155','10.154.105.156'])
check_kafka("Ship - SY", ['10.165.105.154','10.165.105.155','10.165.105.156'])
