#!/bin/sh

HOSTNAME=$(hostname -i)

echo "hostname: "$HOSTNAME

echo "replacing nodeName"
sed -i "s/node-name/$HOSTNAME/g" /user/nrtsearch/nrtsearch-replica-config.yaml

echo "replacing nostname"
sed -i "s/host-name-replica/$HOSTNAME/g" /user/nrtsearch/nrtsearch-replica-config.yaml

echo "starting service"
/user/nrtsearch/build/install/nrtsearch/bin/lucene-server /user/nrtsearch/nrtsearch-replica-config.yaml