#!/bin/bash
#
# SCRIPT:   install-marathon-lb.sh

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

# Check if the JQ program is in the PATH
CMD_FILE=$(which jq)
if [ "$CMD_FILE" == "" ]
then
    echo
    echo " The JSON Query (jq) binary is not installed or not in your path. Please install it."
    echoZZ
    echo " brew install jq -- on a Mac"
    echo
    echo " Exiting......"
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

# Install the Security Subcommand into the CLI
echo
#dcos package install --yes --cli dcos-enterprise-cli

# Create/Install the Certificate for Marthon-LB
echo
echo " Creating/installing the certificate for Marthon-LB"
echo
echo " Please ignore the message: Failed to execute script dcos-security"
echo
dcos security org service-accounts keypair -l 4096 marathon-lb-external-private-key.pem marathon-lb-external-public-key.pem
dcos security org service-accounts create -p marathon-lb-external-public-key.pem -d "dcos_marathon_lb-external service account" dcos_marathon_lb-external
dcos security org service-accounts show dcos_marathon_lb-external
curl -skSL -X PUT -H 'Content-Type: application/json' -d '{"description": "Marathon Services"}' -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:service:marathon:marathon:services:%252F
curl -skSL -X PUT -H 'Content-Type: application/json' -d '{"description": "Marathon Events"}' -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:service:marathon:marathon:admin:events
curl -skSL -X PUT -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:service:marathon:marathon:services:%252F/users/dcos_marathon_lb-external/read
curl -skSL -X PUT -H "Authorization: token=$(dcos config show core.dcos_acs_token)" $(dcos config show core.dcos_url)/acs/api/v1/acls/dcos:service:marathon:marathon:admin:events/users/dcos_marathon_lb-external/read
dcos security secrets create-sa-secret marathon-lb-external-private-key.pem dcos_marathon_lb-external marathon-lb-external
dcos security secrets list /
dcos security secrets get /marathon-lb-external --json | jq -r .value | jq

# end of script