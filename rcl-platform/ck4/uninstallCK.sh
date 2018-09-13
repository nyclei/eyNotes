#!/bin/bash

##############################################################################
#
# This tool could be run on any node of Mesos cluster, the node should have
# dcos cli installed, e.g. MasterNode1.
# (It can be run under 'root' or 'mesossu')
#
# Another requirement: /janitor docker image should be downloadable from
# cluster's docker registry
#
##############################################################################


# TODO STOP if mesos is on 1.9.5


# JANITOR_IMAGE_PATH='awssandbox.registry.rccl.com:10104/janitor:latest'

if [ -z "$1" ]; then
    echo "Missing Janitor image path"
    echo " Usage:   ./uninstallCK.sh [JanitorImagePath]  "
    echo " Example:"
    echo "   ./uninstallCK.sh 'awssandbox.registry.rccl.com:10104/janitor:latest'             # -- AwsSanbox"
    echo "   ./uninstallCK.sh 'tst2-registry.nowlab.tstsh.tstrccl.com:10104/janitor:latest'   # -- ShipTst"
    echo "   ./uninstallCK.sh 'shiptst2.registry.rccl.com:10104:10104/janitor:latest'         # -- ShipTst2"
    echo "   ./uninstallCK.sh 'registry.allure.sh.rccl.com:10104/janitor:latest'              # -- Ship AL"
    echo "   ./uninstallCK.sh 'dev2.registry.rccl.com:10104/janitor:latest'                   # -- AwsDev2"
    echo "   ./uninstallCK.sh 'tst2.registry.rccl.com:10104/janitor:latest'                   # -- AwsTst2"
    echo "   ./uninstallCK.sh 'stg1.registry.rccl.com:10104/janitor:latest'                   # -- AwsStage"
    echo "   ./uninstallCK.sh 'stg-registry.nowlab.tstsh.tstrccl.com:10104/janitor:latest'    # -- ShipStage"
    echo "   ./uninstallCK.sh 'prd.registry.rccl.com:10104/janitor:latest'                    # -- AwsProd"
    exit 1
fi

JANITOR_IMAGE_PATH=$1

# pre-pull the docker image
imagesNo=$(docker images --format {{.Repository}}:{{.Tag}} |grep 'janitor'| grep -c $JANITOR_IMAGE_PATH)
if [ $imagesNo -lt 1 ]; then
    echo "> docker pull $JANITOR_IMAGE_PATH"
    docker pull '$JANITOR_IMAGE_PATH'
fi

echo
echo "!!! Uninstalling Confluent kafka services will remove all topic data !!!"
echo
read -p "Press any key to continue? (Ctrl-C to exit)"

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

# Uninstall Kafka Connect services
dcos marathon app list --quiet | grep '/confluent/connect' | while read -r line ; do
    echo "> dcos marathon app remove --force $line"
    dcos marathon app remove --force $line
    sleep 10
done

# Uninstall Rest Proxy service
if [ "$(dcos marathon app list --quiet | grep -c '/confluent/rest-proxy')" -eq 1 ]; then
    echo '> dcos marathon app remove --force /confluent/rest-proxy'
    dcos marathon app remove --force /confluent/rest-proxy
    sleep 10
fi

# Uninstall Schema Registry service
if [ "$(dcos marathon app list --quiet | grep -c '/confluent/schema-registry')" -eq 1 ]; then
    echo '> dcos marathon app remove --force /confluent/schema-registry'
    dcos marathon app remove --force /confluent/schema-registry
    sleep 10
fi

# Uninstall the rest of services inside '/confluent' group
dcos marathon app list --quiet | grep '/confluent/' | while read -r line ; do
    echo "> dcos marathon app remove --force $line"
    dcos marathon app remove --force $line
    sleep 10
done

# Remove the group /confluent
if [ "$(dcos marathon group list | grep -c '/confluent')" -eq 1 ]; then
    echo
    read -r -p "Remove empty group of /confluent?  [y/N] " response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
    then
        echo '> dcos marathon group remove /confluent'
        dcos marathon group remove /confluent 2>&1 >/dev/null
    fi
fi

# Uninstall /confluent-kafka
if [ "$(dcos marathon app list --quiet | grep -c '/confluent-kafka')" -eq 1 ]; then
    echo '> dcos package uninstall confluent-kafka --yes'
    dcos package uninstall confluent-kafka --yes
    echo
    echo "Waiting for brokers being killed..."
    echo "Please check exhibitor for zkNode: /dcos-service-confluent-kafka"
    echo "... ..."
    sleep 10
    echo "... ..."
    sleep 10
    echo "... ..."
    sleep 10
    echo "... ..."
    sleep 10
fi

# Clean up
echo
read -r -p "Start Janitor to do clean up?  [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    docker run $JANITOR_IMAGE_PATH /janitor.py -r confluent-kafka-role -p confluent-kafka-principal -z dcos-service-confluent-kafka
    echo '...' && echo && sleep 10
fi


echo
echo "ATTENTION:"
echo "  Please check each broker node, the broker service should be killed!"
echo "  Please check exhibitor for successful removal of zkNode:[/dcos-service-confluent-kafka]"
echo "    !!!  YOU MAY HAVE TO MANUALLY REMOVE zkNode:[/dcos-service-confluent-kafka] "
echo "           at http://[master.mesos]/exhibitor/exhibitor/v1/ui/index.html  !!!"
echo
curl -X DELETE http://leader.mesos:8181/exhibitor/v1/explorer/znode/dcos-service-confluent-kafka &> /dev/null
echo
echo "GAME OVER."
