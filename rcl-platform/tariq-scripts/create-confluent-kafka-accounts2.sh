#! /bin/bash

# READ Lei
# The idea of this change is create another secret for 'confluent-kafka2/kafka-secret', this is same secret name used
# in the marathon json file .
# When new namespace of 'confluent-kafka2' is used, all of the "confluent-kafka-role" seems need to
# be changed into "confluent-kafka2-role" as well.


# Commands for provisioning the Kafka Service Account
#
# Mesosphere, All Rights Reserved
#
# This file assumes that the DCOS URL has been set up, if in doublt:
# dcos config show
#
# Create Key Pair
#
#dcos security org service-accounts keypair confluent-kafka-private-key2.pem confluent-kafka-public-key2.pem

#
# Log into DCOS
#
#read -r -p "Do you need to log into DCOS to update your access token [y/N] " response
#if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
#then
#    dcos auth login
#fi


#dcos security org service-accounts create -p confluent-kafka-public-key2.pem -d "Confluent Kafka service account" confluent-kafka-principal

#dcos security org service-accounts show confluent-kafka-principal

dcos security secrets create-sa-secret confluent-kafka-private-key.pem confluent-kafka-principal confluent-kafka2/kafka-secret

#read -r -p "Do you wish to view the secrets in the DCOS Vault [y/N] " response
#if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
#then
#    dcos security secrets list /
#fi



curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:task:user:nobody -d '{"description":"Allows Linux user nobody to execute tasks"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:framework:role:confluent-kafka2-role -d '{"description":"Controls the ability of confluent-kafka2-role to register as a framework with the Mesos master"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:role:confluent-kafka2-role -d '{"description":"Controls the ability of kafka-role to reserve resources"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:role:confluent-kafka2-role -d '{"description":"Controls the ability of kafka-role to access volumes"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:principal:confluent-kafka-principal -d '{"description":"Controls the ability of confluent-kafka-principal to reserve resources"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:principal:confluent-kafka-principal -d '{"description":"Controls the ability of confluent-kafka-principal to access volumes"}' -H 'Content-Type: application/json'

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:framework:role:confluent-kafka2-role/users/confluent-kafka-principal/create

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:role:confluent-kafka2-role/users/confluent-kafka-principal/create

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:role:confluent-kafka2-role/users/confluent-kafka-principal/create

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:task:user:nobody/users/confluent-kafka-principal/create

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:reservation:principal:confluent-kafka-principal/users/confluent-kafka-principal/delete

curl -X PUT -k -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:mesos:master:volume:principal:confluent-kafka-principal/users/confluent-kafka-principal/delete
