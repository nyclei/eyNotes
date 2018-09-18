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

BACKUP_FILENAME='./backupConnectors.txt'

curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_shore_to_ship_replicator_incremental_v18 > $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_birthdate_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_email_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_stateroom_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_consumer_id_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_bkgid_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME &&
echo >> $BACKUP_FILENAME &&
curl --request GET --url http://10.135.105.158:10110/connectors/cdc_bookings_by_alternate_email_cassandra_sink_connector_incremental_v18 >> $BACKUP_FILENAME
