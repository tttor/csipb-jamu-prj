#!/bin/bash
#TODO; use for loop

################################################################################
echo "Starting IJAH web..."
docker run --restart=always -d --name "ijahweb_daemon" -p 2002:80 -v /home/ijah/ijah/web:/var/www/html ijah

################################################################################
echo "Starting IJAH predictor server 0"

serverId=0
LBHostToListenFrom=0.0.0.0
LBPortToListenFromLo=5010
LBPortToListenFromHi=5015
server=/ijah-predictor/predictor/server/server.py

docker run --restart=always -d --name "ijah_predictor_0_daemon" -p $LBPortToListenFromLo-$LBPortToListenFromHi:$LBPortToListenFromLo-$LBPortToListenFromHi -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi

################################################################################
echo "Starting IJAH predictor server 1"

serverId=1
LBHostToListenFrom=0.0.0.0
LBPortToListenFromLo=5020
LBPortToListenFromHi=5025
server=/ijah-predictor/predictor/server/server.py

docker run --restart=always -d --name "ijah_predictor_1_daemon" -p $LBPortToListenFromLo-$LBPortToListenFromHi:$LBPortToListenFromLo-$LBPortToListenFromHi -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi

################################################################################
echo "Starting IJAH predictor server 2"

serverId=2
LBHostToListenFrom=0.0.0.0
LBPortToListenFromLo=5030
LBPortToListenFromHi=5035
server=/ijah-predictor/predictor/server/server.py

docker run --restart=always -d --name "ijah_predictor_2_daemon" -p $LBPortToListenFromLo-$LBPortToListenFromHi:$LBPortToListenFromLo-$LBPortToListenFromHi -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi

################################################################################
echo "Starting IJAH predictor server 3"

serverId=3
LBHostToListenFrom=0.0.0.0
LBPortToListenFromLo=5040
LBPortToListenFromHi=5045
server=/ijah-predictor/predictor/server/server.py

docker run --restart=always -d --name "ijah_predictor_3_daemon" -p $LBPortToListenFromLo-$LBPortToListenFromHi:$LBPortToListenFromLo-$LBPortToListenFromHi -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $server $serverId $LBHostToListenFrom $LBPortToListenFromLo $LBPortToListenFromHi

################################################################################
# LB should be started after all predictor servers up
echo "Starting IJAH load balancer..."

phpApiHost=0.0.0.0
phpApiPort=5000
serverHost=172.18.79.22
serverPortLo=5010
serverPortHi=5015
LB=/ijah-predictor/predictor/server/load_balancer.py

docker run --restart=always -d --name "ijah_loadbalancer_daemon" -p $phpApiPort:$phpApiPort -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u $LB $phpApiHost $phpApiPort $serverHost $serverPortLo $serverPortHi
