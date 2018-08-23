#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Missing ship networking IP4[2nd]"
    echo "   Usage: ./validate-ship.sh [164|127|168|###]"
    exit 1
fi

NETWORK="10.$1.105.15"
JUMP="ssh -q 7001733@10.14.31.247"
#JUMP="eval "

echo "==> Zookeeper"
result=`$JUMP "porttest ${NETWORK}1 2181"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}1 2181 => ${result}"
result=`$JUMP "porttest ${NETWORK}2 2181"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}2 2181 => ${result}"
result=`$JUMP "porttest ${NETWORK}3 2181"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}3 2181 => ${result}"
echo

echo "==> AWS Production"
result=`ssh -q ${NETWORK}4 'porttest 10.17.121.6 2181'`
echo "[From ${NETWORK}4] :  porttest 10.17.121.6 2181 => ${result}"
result=`ssh -q ${NETWORK}5 'porttest 10.17.121.6 2181'`
echo "[From ${NETWORK}5] :  porttest 10.17.121.6 2181 => ${result}"
result=`ssh -q ${NETWORK}6 'porttest 10.17.121.6 2181'`
echo "[From ${NETWORK}6] :  porttest 10.17.121.6 2181 => ${result}"
result=`ssh -q ${NETWORK}7 'porttest 10.17.121.6 2181'`
echo "[From ${NETWORK}7] :  porttest 10.17.121.6 2181 => ${result}"

result=`ssh -q ${NETWORK}4 'porttest 10.17.121.64 2181'`
echo "[From ${NETWORK}4] :  porttest 10.17.121.64 2181 => ${result}"
result=`ssh -q ${NETWORK}5 'porttest 10.17.121.64 2181'`
echo "[From ${NETWORK}5] :  porttest 10.17.121.64 2181 => ${result}"
result=`ssh -q ${NETWORK}6 'porttest 10.17.121.64 2181'`
echo "[From ${NETWORK}6] :  porttest 10.17.121.64 2181 => ${result}"
result=`ssh -q ${NETWORK}7 'porttest 10.17.121.64 2181'`
echo "[From ${NETWORK}7] :  porttest 10.17.121.64 2181 => ${result}"
echo


echo "==> AWS Production 9092"
result=`ssh -q ${NETWORK}4 'porttest 10.17.125.74 9092'`
echo "[From ${NETWORK}4] :  porttest 10.17.125.74 9092 => ${result}"
result=`ssh -q ${NETWORK}5 'porttest 10.17.125.74 9092'`
echo "[From ${NETWORK}5] :  porttest 10.17.125.74 9092 => ${result}"
result=`ssh -q ${NETWORK}6 'porttest 10.17.125.74 9092'`
echo "[From ${NETWORK}6] :  porttest 10.17.125.74 9092 => ${result}"
result=`ssh -q ${NETWORK}7 'porttest 10.17.125.74 9092'`
echo "[From ${NETWORK}7] :  porttest 10.17.125.74 9092 => ${result}"
echo 

# reverse
echo "==> AWS Production probing back - ZK"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}1 2181"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}1 2181 => ${result}"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}2 2181"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}2 2181 => ${result}"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}3 2181"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}3 2181 => ${result}"
echo

# reverse
echo "==> AWS Production probing back - broker"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}4 9092"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}4 9092 => ${result}"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}5 9092"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}5 9092 => ${result}"
result=`ssh -q 10.17.121.6 "porttest ${NETWORK}6 9092"`
echo "[From 10.17.121.6] :  porttest ${NETWORK}6 9092 => ${result}"
echo

echo "==> AEM Publish Server Host"
result=`ssh -q ${NETWORK}8 'porttest 172.23.60.43 4503'`
echo "[From ${NETWORK}8] :  porttest 172.23.60.43 4503 => ${result}"
result=`ssh -q ${NETWORK}9 'porttest 172.23.60.43 4503'`
echo "[From ${NETWORK}9] :  porttest 172.23.60.43 4503 => ${result}"
echo

echo "==> AEM Content"
result=`ssh -q ${NETWORK}8 "curl -kIsS http://172.23.60.43:4503/content/excalibur/en/ships.1.json | grep \"HTTP/1.1 200 OK\""`
echo "[From ${NETWORK}8] :  curl /ships => ${result}"
result=`ssh -q ${NETWORK}9 "curl -kIsS http://172.23.60.43:4503/content/excalibur/en.1.json | grep \"HTTP/1.1 200 OK\""`
echo "[From ${NETWORK}9] :  curl /en => ${result}"
echo

echo "==> Kafka Broker (Test after Kafka installed)"
result=`$JUMP "porttest ${NETWORK}4 9092"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}4 9092 => ${result}"
result=`$JUMP "porttest ${NETWORK}5 9092"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}5 9092 => ${result}"
result=`$JUMP "porttest ${NETWORK}6 9092"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}6 9092 => ${result}"
result=`$JUMP "porttest ${NETWORK}7 9092"`
echo "[From 10.14.31.247] :  porttest ${NETWORK}7 9092 => ${result}"
echo
