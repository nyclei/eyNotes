#!/usr/bin/python

import requests
import json
import sys
import os


publicNodeUrl = "http://10.17.125.74:13569/connectors"
publicNodeUrl = "http://10.17.121.235:10109/connectors"


TEMPFILE = "./connector-topic-map.json"

if (len(sys.argv) > 1):
    publicNodeUrl = sys.argv[1]

connectors = [
    "ga-profile-bookings-b-replicator-SY-v1",
    "deck_list_source_prod_v1",
    "guest_accounts_verify_loyalty_v1_eq_replicator",
    "voyages_olci_status_sink_prod_v2",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_pr_replicator",
    "generics_sink_prod_v1",
    "cdc_bookings_by_bkgid_sink_connector_prod_incremental_v15",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_sr_replicator",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_al_replicator",
    "voyage_info_source_prod_v3",
    "voyage_info_source_prod_v2",
    "ga-postal-optins-b-sink-connector-v1",
    "current_voyage_ship_to_shore_replicator_oa_prod",
    "cdc_bookings_sql_source_connector_prod_incremental_v15",
    "cdc_bookings_by_email_sink_connector_prod_incremental_v15",
    "ga-postal-optins-b-replicator-SY-v1",
    "current_voyage_ship_to_shore_replicator_al_prod",
    "ship_list_sink_prod_v2",
    "ga-postal-optins-b-replicator-EQ-v1",
    "ga-postal-optins-b-replicator-ID-v1",
    "deck_list_sink_prod_v1",
    "port_info_source_prod_v1",
    "current_voyage_ship_to_shore_replicator_ad_prod",
    "ga-postal-optins-b-replicator-AL-v1",
    "ga-profile-bookings-b-replicator-ID-v2",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_sy_replicator",
    "ga-postal-optins-b-replicator-CS-v1",
    "ga-postal-optins-b-replicator-EN-v1",
    "commerce_ship_to_shore_replicator_MA",
    "current_voyage_ship_to_shore_replicator_cs_prod",
    "ship_list_source_prod_v2",
    "ga-update-loyalty-EQ-to-shore-replicator-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_hm_replicator",
    "ship_time_ship_to_shore_replicator_prod_eq_v2",
    "ga-profile-bookings-b-sink-connector-v2",
    "ga-profile-bookings-b-sink-connector-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_cs_replicator",
    "cdc_bookings_by_stateroom_sink_connector_prod_incremental_v15",
    "commerce_ship_to_shore_replicator_v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_ad_replicator",
    "cdc_bookings_sql_source_connector_prod_incremental_v15_2",
    "commerce_product_deltas",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_br_replicator",
    "current_voyage_ship_to_shore_replicator_rf_prod",
    "commerce_ship_to_shore_replicator_EN",
    "ship_time_ship_to_shore_replicator_prod_sy_v2",
    "cdc_bookings_by_alternate_email_cassandra_sink_connector_prod_incremental_v15",
    "commerce_ship_to_shore_replicator_EQ",
    "voyage_list_sink_prod_v3",
    "commerce_ship_to_shore_replicator_EG",
    "voyage_list_sink_prod_v2",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_eq_replicator",
    "commerce_ship_to_shore_replicator_v1_OA",
    "ship_time_ship_to_shore_replicator_prod_al_v2",
    "commerce_ship_to_shore_replicator_MJ",
    "voyages_olci_status_source_prod_v2",
    "ship_time_ship_to_shore_replicator_prod_en_v2",
    "voyage_list_source_prod_v3",
    "current_voyage_ship_to_shore_replicator_hm_prod",
    "voyage_list_source_prod_v2",
    "ga-profiles-optins-b-sink-connector-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_oa_replicator",
    "ga-postal-optins-b-replicator-OA-v1",
    "ga-profile-bookings-b-replicator-RF-v2",
    "ga-profile-bookings-b-replicator-SR-v2",
    "ga-profile-bookings-b-replicator-MA-v2",
    "ga-postal-optins-b-replicator-MA-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_ma_replicator",
    "guest_accounts_verify_loyalty_v1_cs_replicator",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_mj_replicator",
    "commerce_ship_to_shore_replicator_CS",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_en_replicator",
    "ga-profile-bookings-b-replicator-CS-v2",
    "folio-cassandra-sink-prod-v1",
    "current_voyage_ship_to_shore_replicator_sy_prod",
    "ga-profile-bookings-b-replicator-OA-v2",
    "ship_time_ship_to_shore_replicator_prod_sr_v2",
    "ship_time_ship_to_shore_replicator_prod_hm_v2",
    "ship_time_ship_to_shore_replicator_prod_rf_v2",
    "commerce_ship_to_shore_replicator_SY",
    "ship_time_ship_to_shore_replicator_prod_cs_v2",
    "ga-postal-optins-b-replicator-AD-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_id_replicator",
    "cdc_bookings_by_consumer_id_cassandra_sink_connector_incremental_v15",
    "guest_account_link_loyalty_prod_v1_replicator",
    "ship_time_ship_to_shore_replicator_prod_oa_v2",
    "generics_source_prod_v1",
    "guest_accounts_legacy_link_booking_prod_v1_al_replicator",
    "guest_accounts_verify_loyalty_v1_ad_replicator",
    "voyage_info_sink_prod_v2",
    "voyage_info_sink_prod_v3",
    "port_info_sink_prod_v1",
    "ga-profile-bookings-b-replicator-EQ-v2",
    "cdc_bookings_by_birthdate_sink_connector_prod_incremental_v15",
    "ship_time_sink_prod_v2",
    "ga-profile-bookings-b-replicator-AL-v2",
    "commerce_ship_to_shore_replicator_v1_SR",
    "ship_stats_by_ship_code_sink_prod_v1",
    "current_voyage_ship_to_shore_replicator_en_prod",
    "ga-profile-bookings-a-shore-source-connector-v1",
    "guest_accounts_search_add_loyalty_ucm_prod_v1_rf_replicator",
    "commerce_ship_to_shore_replicator_RF",
    "current_voyage_ship_to_shore_replicator_eq_prod",
    "ga-profile-bookings-b-replicator-AD-v2",
    "ship_location_sink_prod_v1",
    "ga-postal-optins-b-replicator-SR-v1",
    "commerce_ship_to_shore_replicator_AD",
    "ga-profile-bookings-b-replicator-EN-v2",
    "guest_accounts_legacy_link_booking_prod_v1_sy_replicator",
    "current_voyage_ship_to_shore_replicator_mj_prod",
    "ga-postal-optins-b-replicator-RF-v1"
]

connectors2 = [
    "ga-profile-bookings-b-replicator-AD-v2",
    "ship_location_sink_prod_v1",
    "ga-postal-optins-b-replicator-SR-v1",
    "commerce_ship_to_shore_replicator_AD",
    "ga-profile-bookings-b-replicator-EN-v2",
    "guest_accounts_legacy_link_booking_prod_v1_sy_replicator",
    "current_voyage_ship_to_shore_replicator_mj_prod",
    "ga-postal-optins-b-replicator-RF-v1"
]

output = []
for connector in connectors:
    print
    url=publicNodeUrl+"/"+connector
    print "URL ==> " + url
    resp=requests.request('GET', url)

    try:
        jsonData = json.loads(resp.text)
        config = jsonData.get('config')
        topics = str(config.get('topic.whitelist'))+","+str(config.get('topics'))
        topicList = topics.split(",")
        for t in topicList:
            if t=="None":
                continue
            # print t
            # print '"'+connector+'",'+'"'+topic+'"'
            element={}
            element["connector"]=connector
            element["topic"]=t
            output.append(element)
    except:
        print '   X -> Failed to decode topic for connector ['+connector+']'

print
print
content = str(output).replace("'","\"")
print content
with open(TEMPFILE, "a+") as f:
    f.write(content)
