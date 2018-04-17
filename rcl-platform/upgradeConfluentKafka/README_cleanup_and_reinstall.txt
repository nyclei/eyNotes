A little background story: 
  There is no simple way to uninstall 'confluent-kafka 1.1.19.1" from dashboard cleanly. Following steps were added here and they can be launched from Jumpbox (or any box which has accesses to the cluster). 

( If you read the scripts in this folder, you will see that there are some ssh steps for remotely controling the nodes. We may have better way to automate everything in the future with Ansible, for now we just built things in old way) 

Start from Jumobox:
1) Before destroy existing Confluent-Kafka from dashboard
   > ssh [master.mesos.IP] "dcos confluent-kafka endpoints broker"
   e.g. > ssh 10.16.4.179 "dcos confluent-kafka endpoints broker"
   Write down all broker ipAddress, write down dockerRegitryIP
2) Destroy 'confluent-kafka' from dashboard   # or use 'dcos' cli command to destroy it
3) For each broker:
   > ./kill-broker.sh [brokerIP]

4) > janitor-clean-by-ip.sh [dockerRegitryIP]
   e.g. ./janitor-clean-by-ip.sh 10.16.7.73
5) > ssh [masterNodeWithDCOS]
6) > dcos package install confluent-kafka --package-version=2.0.$3-3.3.1e --app-id="confluent-kafka-2.0.3-3.3.1e"  --yes  

7) Go to confluent-kafka service, edit its config and set BROKER_PORT to 9092, 
8) Deploy new configuration
