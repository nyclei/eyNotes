#!/bin/bash
echo "Require 'root' permission"

REPO_URL=shiptst2.registry.rccl.com
BOOTSTRAPSERVER=10.16.5.149

DOMAIN_CRT=domain.crt
REPO_PORT=10104
rm -f domain.crt* registry.pem*
wget http://${BOOTSTRAPSERVER}:8404/domain.crt
wget http://${BOOTSTRAPSERVER}:8404/registry.pem
mkdir -p /etc/docker/certs.d/${REPO_URL}:${REPO_PORT}
cp ${DOMAIN_CRT} /etc/docker/certs.d/${REPO_URL}:${REPO_PORT}/ca.crt
# RHEL
cp ${DOMAIN_CRT} /etc/pki/ca-trust/source/anchors/${REPO_URL}.crt
echo "Updating CA trust"
update-ca-trust
# This is for DCOS version 1.8 and lower only
CACERT=/opt/mesosphere/active/python-requests/lib/python3.5/site-packages/requests
echo "Hack for 1.8 cacerts"
cp  ${CACERT}/{cacert.pem,cacert.pem.bup}
cat registry.pem >> ${CACERT}/cacert.pem
systemctl restart docker

