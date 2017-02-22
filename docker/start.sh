#!/bin/bash

echo "Starting IJAH web..."
docker run --restart=always -d --name "ijahweb_daemon" -p 2002:80 -v /home/ijah/ijah/web:/var/www/html ijah

echo "Starting IJAH load balancer..."
docker run --restart=always -d --name "ijah_loadbalancer_daemon" -p 5000:5000 -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u /ijah-predictor/server/load_balancer.py 0.0.0.0 5000 172.18.79.22 5010 5015 5

echo "Starting IJAH predictor server 0"
docker run --restart=always -d --name "ijah_predictor_0_daemon" -p 5010-5012:5010-5012 -v /home/ijah/ijah-predictor/python:/ijah-predictor ijahpredictor python -u /ijah-predictor/server/server.py 0 0.0.0.0 5010 5012

