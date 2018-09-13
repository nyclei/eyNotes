#!/usr/bin/python

import requests
import json
import sys
import os
import sys
from subprocess import check_output
import time

TEMPFILE="./connector-topic-map.json"

with open(TEMPFILE) as f:
    data = json.load(f)

# kt group -brokers 10.16.6.71:9092 -group connect-cdc_bookings_by_email_sink_connector_prod_incremental_v15 -topic cdc_bookings_prod_incremental_v15
awsDev2_brokers='10.16.6.71:9092'
prod_brokers='10.17.125.74:9092,10.17.121.27:9092,10.17.122.121:9092'

cmd=["kt", "group", "-brokers", prod_brokers, "-group", "connect-cdc_bookings_by_email_sink_connector_prod_incremental_v15", "-topic","cdc_bookings_prod_incremental_v15"]
json=check_output(cmd)
#print json
