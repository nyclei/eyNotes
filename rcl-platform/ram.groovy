package connectors

import groovy.json.*
import java.time.*


def     targetmap = ["aws-dev": "http://10.16.4.8/kafka-connect"]
        targetmap = ["awsdevds2": "http://10.16.7.54/connectds2"]
        targetmap << ["aws-stage" : "http://10.17.131.92:10109/kafka-connect"]
        targetmap << ["aws-prod" : "http://10.17.121.235:10109/kafka-connect"]
        targetmap << ["ship-test" : "http://tst1-mesos.nowlab.tstsh.tstrccl.com/kafka-connect"]
        targetmap << ["ship-stage" : "http://10.137.105.158:10109/kafka-connect"]
        targetmap << ["aws-prod" : "http://10.17.121.235:10109"]
        targetmap << ["ship-al" : "http://10.154.105.158:10109/kafka-connect"]
        targetmap << ["ship-sy" : "http://10.165.105.158:10109"]
        targetmap << ["ship-oa" : "http://10.150.105.158:10109/kafka-connect"]
        targetmap << ["ship-eq" : "http://10.149.105.158:10109/kafka-connect"]
        targetmap << ["ship-co" : "http://10.142.105.158:10109/kafka-connect"]      // Complete
        targetmap << ["ship-ha" : "http://10.164.105.158:10109/kafka-connect"]
        targetmap << ["ship-ed" : "http://10.166.105.158:10109/kafka-connect"]
        targetmap << ["ship-sr" : "http://10.130.105.158:10109/kafka-connect"]      // Complete
targetmap << ["ship-en" : "http://mesos.enchantment.sh.rccl.com/kafka-connect"]


// setups
def env = "ship-stage"

def getTime() {
    LocalDateTime t = LocalDateTime.now();
    return ( t.dayOfYear+":"+t.hour+":"+t.minute)
}

target = targetmap.getAt(env)

def options = ["targetenv": env]
    options << ["targeturl": target]
    options << ["onlycassandra" : "0"]
    options <<  ["onlystatus" : "1"]

// def connectorstatefile = new File('connectors/status/'+env+'-'+getTime()+'.txt')
def connectorstatefile = new File('connectors/status/'+env+'.txt')
connectorstatefile << "Target Environment:\t"+env + "\t" + target
println(getTime()+" --- Target Environment:\t"+env + "\t" + target)
ProcessList(options,connectorstatefile)

def ProcessList(Map<String,String> options, File connectorstatefile ) {
    def target = options.getAt("targeturl")
    def response = ["curl", "-k", "-X", "GET", "$target/connectors"].execute().text
    // def response = '["voyage_list_sink_stage_v2_1","folio-cassandra-sink-stage","ship_list_sink_stage_v1","ship_list_sink_stage_v2","ga-enrollment-track-a-shore-source-connector-v1","ga-profiles-optins-b-sink-connector-v1","generics_sink_stage_v1","ship_time_ship_to_shore_replicator_stage_v1","port_info_source_stage_v1","generics_source_stage_v1","voyage_list_source_stage_v2_1","guest_account_verify_loyalty_stage_v1_replicator","ga-profile-bookings-b-sink-connector-v1","guest_profile_link_booking_analytics_stage_ship_to_shore_replicator_v1","guest_account_link_loyalty_stage_v1_replicator","ship_time_al_stage_v1","port_info_sink_stage_v1","ship_list_source_stage_v2","ship_list_source_stage_v1","ga-postal-optins-a-shore-source-connector-v1","commerce_ship_to_shore_replicator_v1_AL","ga-postal-optins-b-sink-connector-v1","voyage_info_source_stage_v2_1","ga-profile-bookings-b-replicator-AL-v1","ga-profiles-optins-b-replicator-AL-v1","ga-postal-optins-b-replicator-v1","ga-enrollment-ship-stage-to-shore-replicator-v1","ga-profile-bookings-a-shore-source-connector-v1","ga-profiles-b-sink-connector-v1","ship_location_sink_stage_v1","discover_efc_current_voyage_replicator_v1","ship_time_sink_stage_v1","deck_list_sink_stage_v1","ga-enrollment-track-b-sink-connector-v1","ga-profiles-b-replicator-AL-v1","ship_stats_by_ship_code_sink_stage_v1","deck_list_source_stage_v1","guest_link_booking_event_stage_v1_replicator","efc_ship_time_sink_stage_v1","voyage_info_sink_stage_v2_1","ga-profiles-optins-a-shore-source-connector-v1","ga-profiles-a-shore-source-connector-v1","ga-enrollment-track-b-replicator-v1"]'
    def connectors = response.replace('[', '').replace(']', '').split(',')
    def i = 0
    for (String connector : connectors) {
        i = i + 1
        connector = connector.replace('"', '')
        println("Processing:" + i + "   " + connector )
        processConnectorStatus(connector,options,connectorstatefile)
    }
}

def processConnector(String connectorname, Map<String,String> options, File connectorstatefile) {

    def target, onlycassandra, onlystatus
    target = options.getAt("targeturl")
    if (options.getAt("onlycassandra")=="1") {onlycassandra = true } else {onlycassandra=false}
    if (options.getAt("onlystatus")=="1") {onlystatus = true } else {onlystatus=false}
    def jsonoutput,out,response


    response = ["curl", "-k", "-X", "GET", "$target/connectors/" + connectorname ].execute().text
    def json = new JsonSlurper().parseText(response)
    def connector_class = json.config.getAt("connector.class")
    def isSource = (connector_class == "com.datamountaineer.streamreactor.connect.cassandra.source.CassandraSourceConnector")
    def isSink = (connector_class == "com.datamountaineer.streamreactor.connect.cassandra.sink.CassandraSinkConnector")
    if (onlystatus) {
        response = ["curl", "-k", "-X", "GET", "$target/connectors/" + connectorname + "/status"].execute().text
    } else {
        response = ["curl", "-k", "-X", "GET", "$target/connectors/" + connectorname ].execute().text
    }
    if ((onlycassandra && (isSink || isSource)) || !onlycassandra){

        jsonoutput = new JsonSlurper().parseText(response)
        if (!onlystatus) {
            connectorstatefile << "$target/" + connectorname + "\n"
            jsonoutput.remove('tasks')
            out = JsonOutput.prettyPrint(JsonOutput.toJson(jsonoutput))
        }
        else {
            out = StringifyJsonStatus(response)
        }
        connectorstatefile << out + "\n"
    }
}

def processConnectorStatus(String connectorname, Map<String,String> options, File connectorstatefile) {

    def target, onlycassandra, onlystatus
    target = options.getAt("targeturl")
    def jsonoutput,out,response
        response = ["curl", "-k", "-X", "GET", "$target/connectors/" + connectorname + "/status"].execute().text
        jsonoutput = new JsonSlurper().parseText(response)
        out = StringifyJsonStatus(response)
        connectorstatefile << out + "\n"
}


def StringifyJsonStatus( String response) {
    println(response)
    def jsonoutput = new JsonSlurper().parseText(response)
    def tasks = jsonoutput.getAt("tasks").iterator().collect {it -> it.getAt("state")}.join('::')
    def connectorname = jsonoutput.getAt("name")
    def connectorstate = jsonoutput.getAt("connector").getAt("state")
    return connectorname+ "," + connectorstate + "," + tasks
}
