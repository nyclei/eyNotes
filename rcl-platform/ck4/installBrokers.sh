#!/bin/bash

##############################################################################
#
# This tool could be run on any node of Mesos cluster, the node should have
# dcos cli installed, e.g. MasterNode1.
# (It can be run under 'root' or 'mesossu')
#
# Another requirement: /kafka-client docker image should be downloadable
# from cluster's docker registry,
#  e.g. /kafka-client:aug2018 is better than old /kafka-client:latest
#
##############################################################################


# KAFKA_CLIENT_IMAGE_PATH='awssandbox.registry.rccl.com:10104/kafka-client:aug2018'

if [ -z "$1" ]; then
    echo "Missing Kafka-client image path"
    echo " Usage:   ./installBrokers.sh [KafkaClientImagePath]  "
    echo " Example:"
    echo "          ./installBrokers.sh 'awssandbox.registry.rccl.com:10104/kafka-client:aug2018'           # -- AwsSanbox"
    echo "          ./installBrokers.sh 'registry.allure.sh.rccl.com:10104/kafka-client:aug2018'            # -- Ship AL"
    echo "          ./installBrokers.sh 'dev2.registry.rccl.com:10104/kafka-client:aug2018'                 # -- AwsDev2"
    echo "          ./installBrokers.sh 'tst2.registry.rccl.com:10104/kafka-client:aug2018'                 # -- AwsTst2"
    echo "          ./installBrokers.sh 'stg1.registry.rccl.com:10104/kafka-client:aug2018'                 # -- AwsStage"
    echo "          ./installBrokers.sh 'stg-registry.nowlab.tstsh.tstrccl.com:10104/kafka-client:aug2018'  # -- ShipStage"
    exit 1
fi

KAFKA_CLIENT_IMAGE_PATH=$1
# pre-pull the docker image
imagesNo=$(docker images --format {{.Repository}}:{{.Tag}} |grep 'kafka-client'| grep -c $KAFKA_CLIENT_IMAGE_PATH)
if [ $imagesNo -lt 1 ]; then
    echo "> docker pull $KAFKA_CLIENT_IMAGE_PATH"
    docker pull '$KAFKA_CLIENT_IMAGE_PATH'
fi


# Check if the DC/OS CLI is in the PATH
CMD_FILE=$(which dcos)
if [ "$CMD_FILE" == "" ]
then
    echo
    echo " The DC/OS Command Line Interface binary is not installed or not in your path. Please install it."
    echo " Exiting."
    echo
    exit 1
fi

# Check if the DC/OS CLI is greater than 0.4.12
CLI_VER=$(dcos --version | grep dcoscli.version | cut -d '=' -f 2)
CLI_VER_MINOR=`echo $CLI_VER | cut -d '.' -f 2 `
CLI_VER_PATCH=`echo $CLI_VER | cut -d '.' -f 3 `
#echo "CLI Minor and Patch == $CLI_VER_MINOR $CLI_VER_PATCH"
if ! [ "$CLI_VER_MINOR" -ge "4" ] && [ "$CLI_VER_PATCH" -ge "13" ]
then
    echo
    echo " Your DC/OS CLI version is not correct. Please upgrade your CLI version."
    echo " Exiting. "
    exit 1
fi

# Check if user is logged into the CLI
while true
do
    AUTH_TOKEN=$(dcos config show core.dcos_acs_token 2>&1)
    if [[ "$AUTH_TOKEN" = *"doesn't exist"* ]]
    then
        echo
        echo " Not logged into the DC/OS CLI. Running login command now. Or press CTL-C "
        echo
        dcos auth login
    else
        break
    fi
done

# Check if the dcos acs token is valid
while true
do
    RESULT=$(dcos node 2>&1)

    if [[ "$RESULT" = *"Your core.dcos_acs_token is invalid"* ]]
    then
        echo
        echo " Your DC/OS dcos_acs_token is invalid. Running login command now. Or press CTRL-C "
        echo
        dcos auth login
    else
        break
    fi
done

# CK4 json

# AwsSandbox
#CPU=0.2      # Unit
#MEM=512      # Unit Mega
#DISK=1000

read -r -p "Broker Count [3~5] (unit): " BROKER_COUNT
BROKER_COUNT=${BROKER_COUNT:-3}
echo " => BROKER_COUNT=$BROKER_COUNT"

read -r -p "Broker CPUs [0.2~12~12] (unit): " BROKER_CPUS
BROKER_CPUS=${BROKER_CPUS:-12}
echo " => BROKER_CPUS=$BROKER_CPUS"

read -r -p "Broker Memory [512~65536~65536] (M): " BROKER_MEM
BROKER_MEM=${BROKER_MEM:-65536}
echo " => BROKER_MEM=$BROKER_MEM"

read -r -p "Broker Disk [1000~460800~2900000] (M): " BROKER_DISK
BROKER_DISK=${BROKER_DISK:-460800}
echo " => BROKER_DISK=$BROKER_DISK"

JVMHEAP=$((BROKER_MEM / 2))  # Unit Mega
CK4_JSON='/tmp/ck4.json'
cat > $CK4_JSON <<- EndOF
{
  "service": {
    "name": "confluent-kafka"
  },
  "brokers": {
    "cpus": $BROKER_CPUS,
    "mem": $BROKER_MEM,
    "heap": {
      "size": $JVMHEAP
    },
    "disk_type": "MOUNT",
    "disk_path": "kafka-broker-data",
    "disk": $BROKER_DISK,
    "count": $BROKER_COUNT,
    "port": 9092,
    "port_tls": 0,
    "kill_grace_period": 30
  },
  "kafka": {
    "compression_type": "snappy",
    "default_replication_factor" : 3,
    "num_partitions": 5,
    "delete_topic_enable": true
  }
}
EndOF


# install CK4 brokers
echo "> dcos package install confluent-kafka --package-version=2.3.0-4.0.0e --options=$CK4_JSON --yes"
dcos package install confluent-kafka --package-version=2.3.0-4.0.0e --options=$CK4_JSON --yes
echo "... ..."
sleep 30
echo "... ..."
sleep 30
echo "... ..."
sleep 30


echo
read -r -p "All 3 kafka brokers are up and running?  [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    echo "Adding default topics..."
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-configs --replication-factor 3 --partitions 1 --config cleanup.policy=compact' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-offsets --replication-factor 3 --partitions 50 --config cleanup.policy=compact' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-status --replication-factor 3 --partitions 10 --config cleanup.policy=compact' &&
    sleep 5
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-cdc-configs --replication-factor 3 --partitions 1 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-cdc-offsets --replication-factor 3 --partitions 50 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-cdc-status --replication-factor 3 --partitions 10 --config cleanup.policy=compact' &&
#    sleep 5
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ga-configs --replication-factor 3 --partitions 1 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ga-offsets --replication-factor 3 --partitions 50 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ga-status --replication-factor 3 --partitions 10 --config cleanup.policy=compact' &&
#    sleep 5
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ncp-configs --replication-factor 3 --partitions 1 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ncp-offsets --replication-factor 3 --partitions 50 --config cleanup.policy=compact' &&
#    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic dcos-connect-ncp-status --replication-factor 3 --partitions 10 --config cleanup.policy=compact' &&
    sleep 5
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --create --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic '_schemas2' --replication-factor 3 --partitions 1' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic _schemas2 --alter --config cleanup.policy=compact' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c './kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka --topic _schemas2 --alter --config min.insync.replicas=2' &&
    sleep 5

    # validation?
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c 'kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka -describe --topic dcos-connect-configs' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c 'kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka -describe --topic dcos-connect-offsets' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c 'kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka -describe --topic dcos-connect-status' &&
    docker run -it $KAFKA_CLIENT_IMAGE_PATH /bin/bash -c 'kafka-topics.sh --zookeeper master.mesos:2181/dcos-service-confluent-kafka -describe --topic _schemas2' &&
    sleep 5

fi
