#!/bin/bash

# ://10.135.105.158:10110/connectors
# [
#   "cdc_bookings_shore_to_ship_replicator_incremental_v18",
#   "cdc_bookings_by_birthdate_cassandra_sink_connector_incremental_v18",
#   "cdc_bookings_by_email_cassandra_sink_connector_incremental_v18",
#   "cdc_bookings_by_stateroom_cassandra_sink_connector_incremental_v18",
#   "cdc_bookings_by_consumer_id_cassandra_sink_connector_incremental_v18",
#   "cdc_bookings_by_bkgid_cassandra_sink_connector_incremental_v18",
#   "cdc_bookings_by_alternate_email_cassandra_sink_connector_incremental_v18"
# ]

TO_PORT="10109"
SHIPTST_1OR2="196"

#1
curl --request POST \
  --url http://10.$SHIPTST_1OR2.105.158:$TO_PORT/connectors \
  --header 'Content-Type: application/json' \
  --data '{"name":"cdc_bookings_shore_to_ship_replicator_incremental_v18", "config":{"connector.class":"io.confluent.connect.replicator.ReplicatorSourceConnector","src.zookeeper.connect":"10.16.4.247:2181/dcos-service-confluent-kafka,10.16.5.137:2181/dcos-service-confluent-kafka,10.16.6.32:2181/dcos-service-confluent-kafka","src.zookeeper.session.timeout.ms":"60000","dest.zookeeper.session.timeout.ms":"60000","tasks.max":"1","dest.zookeeper.connection.timeout.ms":"60000","dest.zookeeper.connect":"master.mesos:2181/dcos-service-confluent-kafka","confluent.license":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJDMDAxMzAiLCJleHAiOjE4MjYyOTMwNDMsImlhdCI6MTUxMDc2MDI0MywiaXNzIjoiQ29uZmx1ZW50IiwibW9uaXRvcmluZyI6dHJ1ZSwibmI0IjoxNTEwNzYwMTIzLCJzdWIiOiJjb250cm9sLWNlbnRlciJ9.ep8lB0y4XH9iZ3OLyB-TNIEZCWCaEB0ZCyuPSH-qMgrj3CFKPa2TtqHt069uXCep83tpXJ6ELnRs-jKFeMhConP0M2KLkuR9TFH4rshQpKeJpX27PHgaPuDPcHCwTbKVHEKx7Mx3vbP3uw6kWpKfgYzfxAnGcbZPUavE9Lh8FTcUdPFooidLpxwCuO0T0dPZfgWV2ti6fAT0GnTfZvc1uGB04QxwL-hd00k6NrkSS4Jt9bmxi7Hq_qY2XTIwfBncNbJ64wcnnwdUs-8krpH6qfDCm2KLEYHJ98niKK_coedkyF8DRL8sEGM_O_3r2sFU5S0SVpc055WNxT5-IVFGCA","src.zookeeper.connection.timeout.ms":"60000","name":"cdc_bookings_shore_to_ship_replicator_incremental_v18","value.converter":"io.confluent.connect.replicator.util.ByteArrayConverter","key.converter":"io.confluent.connect.replicator.util.ByteArrayConverter","topic.whitelist":"cdc_bookings_incremental_v18","src.kafka.bootstrap.servers":"10.16.4.189:9092,10.16.5.11:9092,10.16.6.228:9092"}}'
