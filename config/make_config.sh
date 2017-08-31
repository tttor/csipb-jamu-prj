#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "USAGE:"
  echo "bash make_config.sh [dev/prod]"
  exit 1
fi
MODE=${1}

## database ########################################################################################
echo "making DATABASE config..."
cp "${MODE}_database_config.json" ../database/config_database.json
cp "${MODE}_database_config.json" ../predictor/connectivity/classifier/config_database.json

## predictor ########################################################################################
echo "making PREDICTOR config..."
cp "${MODE}_predictor_config.json" ../predictor/connectivity/classifier/config_predictor.json

## webserver ########################################################################################
echo "making WEBSERVER config..."
cp "${MODE}_webserver_config.ts" ../webserver/src/app/config_webserver.ts
