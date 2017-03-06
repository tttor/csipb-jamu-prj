#!/bin/bash

echo "Stopping IJAH web..."
docker stop ijahweb_daemon
docker rm   ijahweb_daemon

echo "Stopping IJAH loadbalancer..."
docker stop ijah_loadbalancer_daemon
docker rm   ijah_loadbalancer_daemon

echo "Stopping IJAH predictor..."
docker stop ijah_predictor_0_daemon
docker rm   ijah_predictor_0_daemon
