#!/bin/bash

echo "Stopping IJAH web..."
docker stop ijah_web_daemon
docker rm   ijah_web_daemon

echo "Stopping IJAH loadbalancer..."
docker stop ijah_loadbalancer_daemon
docker rm   ijah_loadbalancer_daemon

echo "Stopping IJAH predictor..."
docker stop ijah_predictor_0_daemon
docker rm   ijah_predictor_0_daemon
# docker stop ijah_predictor_1_daemon
# docker rm   ijah_predictor_1_daemon
# docker stop ijah_predictor_2_daemon
# docker rm   ijah_predictor_2_daemon
# docker stop ijah_predictor_3_daemon
# docker rm   ijah_predictor_3_daemon
