#!/bin/bash

################################################################################
echo "Starting IJAH web..."
docker run --restart=always -d --name "ijahweb_daemon" -p 2002:80 -v /home/ijah/ijah/web:/var/www/html ijah

################################################################################
echo "Starting IJAH load balancer..."

waitingTime=5
phpApiHost=0.0.0.0
phpApiPort=5000
serverHost=172.18.79.22
serverPortLo=5010
serverPortHi=5015
LB=/ijah-predictor/server/load_balancer.py

docker run --restart=always -d --name "ijah_loadbalancer_daemon" -p $phpApiPort:phpApiPort -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $LB $phpApiHost $phpApiPort $serverHost $serverPortLo $serverPortHi $waitingTime

################################################################################
echo "Starting IJAH predictor server 0"

serverId=0
LBHostToListenFrom=0.0.0.0
LBPortToListenFromLo=5010
LBPortToListenFromHi=5012
server=/ijah-predictor/server/server.py

docker run --restart=always -d --name "ijah_predictor_0_daemon" -p $LBPortToListenFromLo-$LBPortToListenFromHi:$LBPortToListenFromLo-$LBPortToListenFromHi -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi
